@echo off
cd /d C:\Projects\baby-mania-agent
C:\Users\3024e\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts\phaseA_live_fix.py --mode=dry-run > output\phaseA-dryrun-stdout.txt 2>&1
echo Exit code: %ERRORLEVEL%
