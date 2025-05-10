@echo off
cd /d "D:\CODING\PY\YTDL"
start "" python app.py
timeout /t 5 > nul
start "" http://localhost:5342
