@echo off
echo ==============================================
echo Installing Auto-Commit Bot to Windows Startup
echo ==============================================
echo.

set "SCRIPT_DIR=%~dp0"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_FILE=%STARTUP_FOLDER%\github_autocommit.vbs"

echo Creating background worker...
echo Set WshShell = CreateObject("WScript.Shell") > "%VBS_FILE%"
echo WshShell.Run "python """ ^& "%SCRIPT_DIR%auto_commit.py" ^& """", 0, False >> "%VBS_FILE%"

echo.
echo Success! The script has been added to your Windows startup folder.
echo It will now run completely invisibly in the background every time you turn on your PC.
echo.
echo Note: Remember to add a Git Remote to this folder first by running:
echo git remote add origin ^<YOUR_GITHUB_REPO_URL^>
echo.
pause
