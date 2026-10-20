@echo off
chcp 65001 >nul
if not exist "%APPDATA%\ingetrazo\plugins" mkdir "%APPDATA%\ingetrazo\plugins"
copy /Y "%~dp0emo_thai_ui.py" "%APPDATA%\ingetrazo\plugins\emo_thai_ui.py" >nul
echo EMO Thai Extension installed. Restart IngeTrazo.
echo View - Language - Thai (Thai)
pause
