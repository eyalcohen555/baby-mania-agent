#!/usr/bin/env python3
"""
BabyMania Bridge — Telegram Working Channel
Phase 1+2+3: Notifications + Reply buttons + Task input from phone.

─── Phase 1 — Notifications ──────────────────────────────────────────────────
  - Monitors bridge/status.md every 3 seconds
  - Sends notification ONLY on defined events (not on every file change)

  Notification policy — sends ONLY for:
    STARTED         — status transitions to 'running'
    DONE            — status transitions to 'done' or 'pushed'
    BLOCKED         — status transitions to 'failed'
    QUESTION        — last-result contains a question for the user
    APPROVAL NEEDED — last-result requests approval

─── Phase 2 — Reply Channel ──────────────────────────────────────────────────
  - Inline keyboard buttons on APPROVAL NEEDED / QUESTION / BLOCKED events
  - Button clicks write to bridge/telegram-response.md
  - Free-text replies when in "waiting for reply" state

─── Phase 3 — Task Input ─────────────────────────────────────────────────────
  - Free text from phone → bridge/next-task.md (when bridge is idle)
  - Confirmation buttons before writing task
  - /cancel to remove a queued task
  - /log to see recent task history
  - Task log appended to bridge/task-log.md
  - Bridge-state aware: rejects tasks when bridge is busy

  Commands:
    /start  — הסבר + תפריט
    /ping   — בדוק חיבור
    /status — מצב Bridge
    /result — תוצאה אחרונה
    /cancel — בטל משימה בתור
    /log    — היסטוריית משימות אחרונה

  Free text flow:
    1. User sends text
    2. Bot checks bridge status — if busy → reject
    3. Bot shows confirmation: [שלח משימה] [בטל]
    4. User confirms → Bot writes to next-task.md + logs to task-log.md

─── Requirements ─────────────────────────────────────────────────────────────
  pip install -r scripts/requirements-telegram.txt

  .env:
    TELEGRAM_BOT_TOKEN=<from @BotFather>
    TELEGRAM_CHAT_ID=<from @userinfobot>

  Run:
    python scripts/telegram_bot.py
"""

import os
import threading
from pathlib import Path
from datetime import datetime

import telebot
from dotenv import load_dotenv

# ── Config ─────────────────────────────────────────────────────────────────────

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError(
        "Missing env vars. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env"
    )

BASE_DIR       = Path(__file__).parent.parent
STATUS_FILE    = BASE_DIR / "bridge" / "status.md"
RESULT_FILE    = BASE_DIR / "bridge" / "last-result.md"
RESPONSE_FILE  = BASE_DIR / "bridge" / "telegram-response.md"
TASK_FILE      = BASE_DIR / "bridge" / "next-task.md"
TASK_LOG_FILE  = BASE_DIR / "bridge" / "task-log.md"

POLL_INTERVAL = 3    # seconds between file checks
MAX_MSG_LEN   = 4096 # Telegram message size limit

# Bridge states that mean "busy — don't accept new tasks"
BUSY_STATUSES = {"running", "starting", "waiting_response"}

# ── Bot instance ───────────────────────────────────────────────────────────────

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# ── Phase 2+3 state ───────────────────────────────────────────────────────────

_reply_lock           = threading.Lock()
_waiting_for_reply    = False   # True when user clicked "שלח תשובה"
_pending_event_type   = ""      # APPROVAL | QUESTION | BLOCKED — set when buttons are sent
_pending_task_id      = ""      # task_id that triggered the current prompt
_pending_task_text    = ""      # Phase 3: task text waiting for confirmation

def _set_waiting(val):
    global _waiting_for_reply
    with _reply_lock:
        _waiting_for_reply = val

def _is_waiting():
    with _reply_lock:
        return _waiting_for_reply

def _set_pending_event(event_type):
    global _pending_event_type
    with _reply_lock:
        _pending_event_type = event_type

def _get_pending_event_type():
    with _reply_lock:
        return _pending_event_type

def _set_pending_task_id(tid: str):
    global _pending_task_id
    with _reply_lock:
        _pending_task_id = tid

def _get_pending_task_id() -> str:
    with _reply_lock:
        return _pending_task_id

def _set_pending_task(text):
    global _pending_task_text
    with _reply_lock:
        _pending_task_text = text

def _get_pending_task():
    with _reply_lock:
        return _pending_task_text

def _clear_pending_task():
    global _pending_task_text
    with _reply_lock:
        _pending_task_text = ""

# ── Helpers ────────────────────────────────────────────────────────────────────

def chunk_message(text, limit=MAX_MSG_LEN):
    """Split text into Telegram-safe chunks at newline boundaries."""
    if len(text) <= limit:
        return [text]
    chunks = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break
        split_at = text.rfind("\n", 0, limit)
        if split_at == -1:
            split_at = limit
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")
    return chunks


def send(text):
    """Send plain text to configured chat_id, chunking if over 4096 chars."""
    for chunk in chunk_message(str(text)):
        try:
            bot.send_message(CHAT_ID, chunk)
        except Exception as e:
            print(f"[TG] send error: {e}")


def send_with_markup(text, markup):
    """Send first chunk with markup, remaining chunks as plain text."""
    chunks = chunk_message(str(text))
    try:
        bot.send_message(CHAT_ID, chunks[0], reply_markup=markup)
    except Exception as e:
        print(f"[TG] send error: {e}")
        return
    for chunk in chunks[1:]:
        send(chunk)


def read_file(path):
    """Read file content, return empty string if missing."""
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return f"[read error: {e}]"


def write_response(action, content=""):
    """
    Write user response to bridge/telegram-response.md.
    This is the ONLY file Phase 2 ever writes to.

    Format:
      time:    YYYY-MM-DD HH:MM:SS
      type:    APPROVAL | QUESTION | BLOCKED  (event that triggered the prompt)
      action:  approve | reject | answer | skip | retry | stop
      content: free text (only when action=answer, otherwise empty)

    Safety: if the file already has unread content, abort and warn the user.
    """
    # Safety check — don't overwrite an unread response
    try:
        existing = RESPONSE_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        existing = ""
    if existing:
        send("⚠️ יש כבר תשובה שממתינה למערכת — לא נכתוב עד שתיקרא")
        print(f"[response] blocked overwrite — unread response exists")
        return

    ts         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event_type = _get_pending_event_type()
    task_id    = _get_pending_task_id()
    try:
        RESPONSE_FILE.write_text(
            f"time: {ts}\ntype: {event_type}\ntask_id: {task_id}\naction: {action}\ncontent: {content}\n",
            encoding="utf-8",
        )
        print(f"[response] wrote type={event_type!r} task_id={task_id!r} action={action!r} content={content[:60]!r}")
    except Exception as e:
        print(f"[response] write error: {e}")
        send(f"⚠️ שגיאה בכתיבת תגובה: {e}")


def is_bridge_busy():
    """Check if bridge is currently running a task."""
    content = read_file(STATUS_FILE)
    status, _ = parse_status(content)
    return status in BUSY_STATUSES


def has_queued_task():
    """Check if there's already a task in next-task.md."""
    content = read_file(TASK_FILE)
    return bool(content)


def write_task(task_text):
    """
    Write task to bridge/next-task.md.
    Returns True on success, False if blocked.
    """
    if is_bridge_busy():
        return False
    try:
        TASK_FILE.write_text(task_text, encoding="utf-8")
        log_task(task_text, "QUEUED")
        print(f"[task] wrote task: {task_text[:80]!r}")
        return True
    except Exception as e:
        print(f"[task] write error: {e}")
        return False


def cancel_task():
    """Remove queued task from next-task.md. Returns the removed text or empty."""
    content = read_file(TASK_FILE)
    if not content:
        return ""
    try:
        TASK_FILE.write_text("", encoding="utf-8")
        log_task(content, "CANCELLED")
        print(f"[task] cancelled: {content[:80]!r}")
        return content
    except Exception as e:
        print(f"[task] cancel error: {e}")
        return ""


def log_task(task_text, action):
    """Append entry to bridge/task-log.md."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    preview = task_text.strip().splitlines()[0][:100] if task_text.strip() else "(empty)"
    entry = f"| {ts} | {action} | {preview} |\n"
    try:
        if not TASK_LOG_FILE.exists():
            TASK_LOG_FILE.write_text(
                "| time | action | task |\n|------|--------|------|\n" + entry,
                encoding="utf-8",
            )
        else:
            with open(TASK_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(entry)
    except Exception as e:
        print(f"[task-log] write error: {e}")


def get_recent_log(n=10):
    """Return last N entries from task-log.md."""
    content = read_file(TASK_LOG_FILE)
    if not content:
        return "(אין היסטוריה)"
    lines = content.strip().splitlines()
    # Skip header (first 2 lines)
    entries = lines[2:] if len(lines) > 2 else []
    if not entries:
        return "(אין היסטוריה)"
    return "\n".join(entries[-n:])


def status_emoji(status_line):
    """Map status keyword to emoji."""
    mapping = {
        "idle":     "⏳",
        "running":  "🔄",
        "done":     "✅",
        "failed":   "❌",
        "locked":   "🔒",
        "error":    "🚨",
        "starting": "🚀",
        "pushed":   "📤",
    }
    for key, emoji in mapping.items():
        if key in status_line.lower():
            return emoji
    return "ℹ️"


def parse_status(content):
    """
    Extract (status, detail) from status.md content.
    Ignores the 'time' field — dedup is based on status+detail only.

    Format written by bridge.py:
      status: {state}
      time: {ts}
      detail: {detail}
    """
    status = ""
    detail = ""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("status:"):
            status = line[len("status:"):].strip().lower()
        elif line.startswith("detail:"):
            detail = line[len("detail:"):].strip()
    return status, detail


def extract_field(content: str, field: str) -> str:
    """Extract a single field value from status.md (field: value format)."""
    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith(f"{field.lower()}:"):
            return line.split(":", 1)[1].strip()
    return ""


def extract_snippet(content, event_type, max_len=200):
    """
    Return a short, relevant excerpt from last-result.md for Telegram display.

    APPROVAL_NEEDED — first line containing an approval keyword.
    QUESTION        — first line ending with '?' or containing שאלה:/האם /question.
    Fallback        — first non-empty line, truncated to max_len.
    """
    lines = [l.strip() for l in content.splitlines() if l.strip()]

    if event_type == "APPROVAL_NEEDED":
        approval_kws = [
            "approval needed", "requires approval", "waiting for approval",
            "נדרש אישור", "אישור אייל", "אישור נדרש",
        ]
        for line in lines:
            if any(kw in line.lower() for kw in approval_kws):
                return line[:max_len]

    elif event_type == "QUESTION":
        question_kws = ["question for user", "question:", "שאלה:", "האם "]
        for line in lines:
            stripped = line.strip()
            if stripped.endswith("?") and len(stripped) > 5:
                return stripped[:max_len]
            if any(kw in stripped.lower() for kw in question_kws):
                return stripped[:max_len]

    # Fallback: first non-empty line
    return lines[0][:max_len] if lines else "(אין תוכן)"


def detect_result_event(content):
    """
    Analyze last-result.md content to determine if a notification is warranted.

    Returns:
      'APPROVAL_NEEDED' — result requests explicit approval from user
      'QUESTION'        — result contains a question directed at the user
      None              — no actionable event (no notification)
    """
    if not content:
        return None

    content_lower = content.lower()

    # Approval detection (English + Hebrew)
    approval_kws = [
        "approval needed", "requires approval", "waiting for approval",
        "נדרש אישור", "אישור אייל", "אישור נדרש",
    ]
    if any(kw in content_lower for kw in approval_kws):
        return "APPROVAL_NEEDED"

    # Question detection — explicit keywords
    question_kws = ["question for user", "question:", "שאלה:", "האם "]
    if any(kw in content_lower for kw in question_kws):
        return "QUESTION"

    # Question detection — lines ending with ?
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.endswith("?") and len(stripped) > 5:
            return "QUESTION"

    return None


# ── Phase 2 button senders ─────────────────────────────────────────────────────

def _capture_pending_task_id():
    """Read current task_id from status.md and store as pending."""
    status_content = read_file(STATUS_FILE)
    tid = extract_field(status_content, "task_id")
    _set_pending_task_id(tid)
    return tid


def send_approval_prompt(context_text):
    """⚠️ APPROVAL NEEDED — כפתורים: אשר / דחה"""
    _set_pending_event("APPROVAL")
    tid = _capture_pending_task_id()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("✅ אשר",  callback_data="approve"),
        telebot.types.InlineKeyboardButton("❌ דחה",  callback_data="reject"),
    )
    snippet = extract_snippet(context_text, "APPROVAL_NEEDED")
    id_line = f"task: {tid}\n" if tid else ""
    send_with_markup(f"⚠️ נדרש אישור שלך\n{id_line}\nעל מה האישור:\n{snippet}", markup)


def send_question_prompt(context_text):
    """❓ QUESTION — כפתורים: שלח תשובה / דלג"""
    _set_pending_event("QUESTION")
    tid = _capture_pending_task_id()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("✏️ שלח תשובה", callback_data="reply"),
        telebot.types.InlineKeyboardButton("⏭️ דלג",        callback_data="skip"),
    )
    snippet = extract_snippet(context_text, "QUESTION")
    id_line = f"task: {tid}\n" if tid else ""
    send_with_markup(f"❓ יש שאלה שמחכה לך\n{id_line}\nהשאלה:\n{snippet}", markup)


def send_blocked_prompt(context_text):
    """❌ BLOCKED — כפתורים: נסה שוב / עצור"""
    _set_pending_event("BLOCKED")
    tid = _capture_pending_task_id()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("🔄 נסה שוב", callback_data="retry"),
        telebot.types.InlineKeyboardButton("🛑 עצור",    callback_data="stop"),
    )
    id_line = f"task: {tid}\n" if tid else ""
    send_with_markup(f"❌ המשימה נעצרה\n{id_line}\n{context_text}", markup)


# ── Phase 2 callback handler ───────────────────────────────────────────────────

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Handle all inline keyboard button presses (Phase 2 + Phase 3)."""
    data = call.data

    # ── Phase 2 buttons ──────────────────────────────────────────────────────
    if data == "approve":
        write_response("approve")
        bot.answer_callback_query(call.id, "אושר ✅")
        send("✅ אישור נשלח למערכת")

    elif data == "reject":
        write_response("reject")
        bot.answer_callback_query(call.id, "נדחה ❌")
        send("❌ דחייה נשלחה למערכת")

    elif data == "reply":
        _set_waiting(True)
        bot.answer_callback_query(call.id, "שלח את התשובה שלך")
        send("✏️ שלח את התשובה שלך עכשיו — ההודעה הבאה תישלח ל-Claude")

    elif data == "skip":
        write_response("skip")
        bot.answer_callback_query(call.id, "דולג ⏭️")
        send("⏭️ דילוג נשלח למערכת")

    elif data == "retry":
        write_response("retry")
        bot.answer_callback_query(call.id, "נסה שוב 🔄")
        send("🔄 בקשת ניסיון חוזר נשלחה למערכת")

    elif data == "stop":
        write_response("stop")
        bot.answer_callback_query(call.id, "עוצר 🛑")
        send("🛑 עצירה נשלחה למערכת")

    # ── Phase 3 buttons (task confirmation) ──────────────────────────────────
    elif data == "task_confirm":
        task_text = _get_pending_task()
        if not task_text:
            bot.answer_callback_query(call.id, "אין משימה ממתינה")
            send("⚠️ אין משימה ממתינה לאישור")
            return
        if is_bridge_busy():
            bot.answer_callback_query(call.id, "Bridge עסוק!")
            send("🔒 ה-Bridge עסוק כרגע — נסה שוב אחרי שהמשימה הנוכחית תסתיים")
            _clear_pending_task()
            return
        if write_task(task_text):
            bot.answer_callback_query(call.id, "משימה נשלחה!")
            send(f"📤 משימה נכתבה ל-Bridge:\n{task_text[:200]}")
        else:
            bot.answer_callback_query(call.id, "שגיאה בכתיבה")
            send("⚠️ שגיאה בכתיבת המשימה — נסה שוב")
        _clear_pending_task()

    elif data == "task_cancel":
        _clear_pending_task()
        bot.answer_callback_query(call.id, "בוטל")
        send("❌ המשימה בוטלה — לא נשלחה")

    else:
        bot.answer_callback_query(call.id, "פעולה לא מוכרת")


# ── File monitor thread ────────────────────────────────────────────────────────

def monitor_loop(stop_event):
    """
    Poll bridge/status.md and bridge/last-result.md.
    Send notification ONLY when a defined event occurs.
    Read-only on all bridge files except telegram-response.md.

    Phase 1 event policy (unchanged):
      EVENT_STATUSES whitelist — only running / done / pushed / failed trigger notifications.
      idle / starting / locked / unknown → dedup state updated, no send.

    Phase 2 additions:
      BLOCKED, QUESTION, APPROVAL NEEDED → send with inline keyboard buttons.
    """
    EVENT_STATUSES = {"running", "done", "pushed", "failed"}

    init_status_content = read_file(STATUS_FILE)
    init_result_content = read_file(RESULT_FILE)

    last_status, last_detail = parse_status(init_status_content)

    # Startup result dedup:
    # If the file already has a pending actionable event (APPROVAL/QUESTION),
    # do NOT suppress it — the user may have missed it before the bot restarted.
    # For non-event results, suppress as normal (anti-spam).
    init_event = detect_result_event(init_result_content)
    if init_event in ("APPROVAL_NEEDED", "QUESTION"):
        last_result_sent = ""   # force send on first poll
        print(f"[monitor] pending event on startup: {init_event!r} — will notify")
    else:
        last_result_sent = init_result_content

    print(f"[monitor] started | status={last_status!r} detail={last_detail!r}")

    while not stop_event.is_set():
        result_sent_this_cycle = False
        try:
            # ── Status events ───────────────────────────────────────────────────
            current_status_content = read_file(STATUS_FILE)
            current_status, current_detail = parse_status(current_status_content)

            if (current_status, current_detail) != (last_status, last_detail):
                last_status = current_status
                last_detail = current_detail

                # Hard gate: only process statuses on the event whitelist.
                # idle / starting / locked / unknown → dedup state updated, no send.
                if current_status not in EVENT_STATUSES:
                    pass  # silent consume

                elif current_status == "running":
                    pass  # suppressed — no STARTED/RUNNING notifications per exception policy

                elif current_status in ("done", "pushed"):
                    # Only notify for T2/T3 — T1 tasks complete silently
                    tier    = extract_field(current_status_content, "approval_tier")
                    task_id = extract_field(current_status_content, "task_id")
                    id_str  = f"[{task_id}] " if task_id else ""
                    if tier in ("T2", "T3"):
                        send(f"✅ {id_str}משימה הסתיימה (tier: {tier})\n{current_detail}")
                        current_result = read_file(RESULT_FILE)
                        if current_result and current_result != last_result_sent:
                            result_preview = current_result[:1500]
                            if len(current_result) > 1500:
                                result_preview += "\n\n... (/result לתוצאה מלאה)"
                            send(f"📋 תוצאה:\n{result_preview}")
                            last_result_sent = current_result
                            result_sent_this_cycle = True
                    # T1 done — update dedup state silently
                    elif tier == "T1":
                        print(f"[monitor] T1 DONE [{task_id}] — suppressed per exception policy")

                elif current_status == "failed":
                    # BLOCKED event (Phase 2 — with buttons)
                    task_id     = extract_field(current_status_content, "task_id")
                    id_str      = f"[{task_id}] " if task_id else ""
                    detail_text = current_detail if current_detail else "(אין פרטים)"
                    send_blocked_prompt(f"{id_str}{detail_text}")

            # ── Result events (independent of status) ──────────────────────────
            if not result_sent_this_cycle:
                current_result = read_file(RESULT_FILE)
                if current_result and current_result != last_result_sent:
                    event = detect_result_event(current_result)
                    status_content = read_file(STATUS_FILE)
                    task_id = extract_field(status_content, "task_id")
                    id_prefix = f"[{task_id}]\n" if task_id else ""
                    if event == "APPROVAL_NEEDED":
                        send_approval_prompt(id_prefix + current_result)
                        last_result_sent = current_result
                    elif event == "QUESTION":
                        send_question_prompt(id_prefix + current_result)
                        last_result_sent = current_result
                    else:
                        # Result changed with no actionable event —
                        # update state silently to prevent re-detection loop
                        last_result_sent = current_result

        except Exception as e:
            print(f"[monitor] error: {e}")

        stop_event.wait(POLL_INTERVAL)

    print("[monitor] stopped")


# ── Command handlers ───────────────────────────────────────────────────────────

@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    if str(message.chat.id) != str(CHAT_ID):
        return
    status_content = read_file(STATUS_FILE)
    status, _ = parse_status(status_content)
    emoji = status_emoji(status) if status else "⏳"
    send(
        f"BabyMania Bridge Bot\n"
        f"מצב: {emoji} {status or 'לא ידוע'}\n\n"
        "━━━ פקודות ━━━\n"
        "/status — מצב Bridge + משימה ממתינה\n"
        "/result — תוצאה אחרונה\n"
        "/cancel — בטל משימה בתור\n"
        "/log    — היסטוריית משימות\n"
        "/ping   — בדוק חיבור\n\n"
        "━━━ שליחת משימה ━━━\n"
        "שלח הודעה חופשית → כפתור אישור → Bridge מריץ\n\n"
        "━━━ כפתורים אוטומטיים ━━━\n"
        "⚠️ אישור → אשר / דחה\n"
        "❓ שאלה → שלח תשובה / דלג\n"
        "❌ חסום → נסה שוב / עצור"
    )


@bot.message_handler(commands=["ping"])
def cmd_ping(message):
    if str(message.chat.id) != str(CHAT_ID):
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_content = read_file(STATUS_FILE)
    status, _ = parse_status(status_content)
    send(f"pong — {ts}\nbridge: {status or 'unknown'}")


@bot.message_handler(commands=["status"])
def cmd_status(message):
    """Status + pending task info."""
    if str(message.chat.id) != str(CHAT_ID):
        return
    content = read_file(STATUS_FILE)
    if content:
        first_line = content.splitlines()[0]
        msg = f"{status_emoji(first_line)} סטטוס Bridge\n{content}"
        # Show pending task if any
        pending = read_file(TASK_FILE)
        if pending:
            preview = pending.strip().splitlines()[0][:80]
            msg += f"\n\n📋 משימה ממתינה:\n{preview}"
        send(msg)
    else:
        send("bridge/status.md לא נמצא או ריק")


@bot.message_handler(commands=["result"])
def cmd_result(message):
    """Full raw last-result.md on demand — no filtering."""
    if str(message.chat.id) != str(CHAT_ID):
        return
    content = read_file(RESULT_FILE)
    if content:
        send(f"📋 תוצאה אחרונה:\n{content}")
    else:
        send("bridge/last-result.md לא נמצא או ריק")


@bot.message_handler(commands=["cancel"])
def cmd_cancel(message):
    """Cancel a queued or blocked task."""
    if str(message.chat.id) != str(CHAT_ID):
        return
    status_content = read_file(STATUS_FILE)
    current_status, _ = parse_status(status_content)
    task_id = extract_field(status_content, "task_id")

    if current_status in ("running", "waiting_response"):
        send(f"⚠️ משימה רצה כרגע [{task_id}] — לא ניתן לבטל. שלח 'stop' דרך הכפתורים אם נחסמה.")
        return

    removed = cancel_task()
    if removed:
        id_str = f" [{task_id}]" if task_id else ""
        # Write CANCELLED to response file so bridge can exit cleanly if waiting
        write_response("stop")
        log_task(removed, f"CANCELLED_BY_USER{id_str}")
        send(f"🗑️ משימה בוטלה{id_str}:\n{removed[:200]}")
    else:
        send("אין משימה בתור לביטול — Bridge במצב idle")


@bot.message_handler(commands=["log"])
def cmd_log(message):
    """Show recent task history."""
    if str(message.chat.id) != str(CHAT_ID):
        return
    log_text = get_recent_log(10)
    send(f"📜 היסטוריית משימות:\n\n{log_text}")


@bot.message_handler(func=lambda m: True)
def catch_all(message):
    """
    Free-text handler (Phase 2 + Phase 3).
    Priority:
      1. If waiting for reply (Phase 2 "שלח תשובה") → telegram-response.md
      2. Otherwise → Phase 3 task input flow with confirmation
    """
    if str(message.chat.id) != str(CHAT_ID):
        return

    text = (message.text or "").strip()
    if not text:
        return

    # Phase 2: waiting for reply to a question/approval
    if _is_waiting():
        _set_waiting(False)
        write_response("answer", text)
        send(f"✅ תשובה נשלחה למערכת:\n{text}")
        return

    # Phase 3: treat free text as a new task
    # Guard: bridge must be idle
    if is_bridge_busy():
        send(
            "🔒 ה-Bridge עסוק כרגע — לא ניתן לשלוח משימה חדשה\n"
            "השתמש ב-/status לבדוק מצב"
        )
        return

    # Guard: no double-queuing
    if has_queued_task():
        send(
            "📋 כבר יש משימה בתור שממתינה לריצה\n"
            "השתמש ב-/cancel כדי לבטל אותה קודם"
        )
        return

    # Show confirmation buttons
    _set_pending_task(text)
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("📤 שלח משימה", callback_data="task_confirm"),
        telebot.types.InlineKeyboardButton("❌ בטל",       callback_data="task_cancel"),
    )
    preview = text[:300] + ("..." if len(text) > 300 else "")
    send_with_markup(f"📝 משימה חדשה:\n\n{preview}\n\nלשלוח ל-Bridge?", markup)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"[TG Bot] starting — chat_id={CHAT_ID}")
    send("BabyMania Bridge Bot מחובר ופעיל\nשלח הודעה = משימה חדשה | /help לתפריט")

    stop_event = threading.Event()
    monitor_thread = threading.Thread(
        target=monitor_loop,
        args=(stop_event,),
        daemon=True,
        name="bridge-monitor",
    )
    monitor_thread.start()

    try:
        print("[TG Bot] polling for commands...")
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except KeyboardInterrupt:
        print("[TG Bot] shutting down...")
    finally:
        stop_event.set()
        monitor_thread.join(timeout=5)
        print("[TG Bot] stopped")
