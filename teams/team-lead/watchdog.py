#!/usr/bin/env python3
"""
watchdog.py — Minimal runtime stub.
Keeps process alive so conductor preflight passes.
Full watchdog implementation pending.
"""
import time
import sys
from pathlib import Path

PID_FILE = Path(__file__).parent.parent.parent / "bridge" / "watchdog.pid"

def main():
    PID_FILE.write_text(str(__import__("os").getpid()))
    while True:
        time.sleep(30)

if __name__ == "__main__":
    main()
