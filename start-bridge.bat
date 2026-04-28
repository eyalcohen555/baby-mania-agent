@echo off
cd /d C:\Projects\baby-mania-agent

:: Start watchdog daemon in background (singleton guard prevents duplicates)
start /B python teams\team-lead\watchdog.py --daemon >> logs\watchdog.log 2>&1

:: Start bridge daemon (foreground — keeps the scheduled task alive)
python -u bridge.py >> logs\bridge.log 2>&1
