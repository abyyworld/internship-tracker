@echo off
REM Windows: install the CV helper so it starts when you log in, and open it.
REM
REM The same idea as start-autoapply.command on macOS. It puts a launcher in the
REM Startup folder and registers a logon task, so the helper comes back at every
REM login and this window can be closed.
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Setting up the local Python environment ^(this is a one-time step^)...
  python -m venv .venv
  ".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
  ".venv\Scripts\python.exe" -m pip install --quiet -r requirements-autoapply.txt
)

REM This also brings the checkout up to date before installing - a service
REM pointed at stale code is the failure the whole thing exists to end.
echo Updating the code and installing the CV helper as a background service...
".venv\Scripts\python.exe" -m autoapply install-service

REM Give it a moment, then open the pairing page in the default browser.
timeout /t 4 /nobreak >nul
if exist "private\bridge.token" (
  set /p TOKEN=<private\bridge.token
  start "" "http://127.0.0.1:8765/connect#%TOKEN%"
  echo.
  echo Done. The CV editor is running and will start itself when you log in.
  echo You can close this window - the editor keeps running without it.
) else (
  echo The service did not start. Its output is in private\bridge.log
  type "private\bridge.log" 2>nul
)
endlocal
