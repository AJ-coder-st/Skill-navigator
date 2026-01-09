@echo off
chcp 65001 >nul
title Career Readiness Mentor - Project Manager
color 0A
setlocal enabledelayedexpansion
REM Store base directory path to handle spaces - remove trailing backslash
set "BASE_DIR=%~dp0"
set "BASE_DIR=%BASE_DIR:~0,-1%"
if not defined BASE_DIR set "BASE_DIR=%~dp0."

:MENU
cls
echo ================================================
echo   Career Readiness Mentor - Project Manager
echo ================================================
echo.
echo   [1] Start Backend Server
echo   [2] Start Frontend Server
echo   [3] Start Both Servers
echo   [4] Stop Backend Server
echo   [5] Stop Frontend Server
echo   [6] Stop All Servers ^& Close Windows
echo   [7] Restart Backend Server
echo   [8] Restart Frontend Server
echo   [9] Restart All Servers
echo   [10] Check Server Status
echo   [0] Exit ^& Close All Servers
echo.
echo ================================================
set /p choice="Enter your choice (0-10): "

if "%choice%"=="1" goto START_BACKEND
if "%choice%"=="2" goto START_FRONTEND
if "%choice%"=="3" goto START_ALL
if "%choice%"=="4" goto STOP_BACKEND
if "%choice%"=="5" goto STOP_FRONTEND
if "%choice%"=="6" goto STOP_ALL
if "%choice%"=="7" goto RESTART_BACKEND
if "%choice%"=="8" goto RESTART_FRONTEND
if "%choice%"=="9" goto RESTART_ALL
if "%choice%"=="10" goto CHECK_STATUS
if "%choice%"=="0" goto EXIT
goto MENU

:START_BACKEND
cls
echo Starting Backend Server...
cd /d "%BASE_DIR%\backend"
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    call "venv\Scripts\activate.bat"
    pip install -r requirements.txt -q
) else (
    call "venv\Scripts\activate.bat"
)
set "BACKEND_DIR=%BASE_DIR%\backend"
start "Backend Server - Port 8000" cmd /k "cd /d \"%BACKEND_DIR%\" && \"%BACKEND_DIR%\venv\Scripts\activate.bat\" && python main.py"
timeout /t 2 >nul
echo Backend server started in new window.
echo.
pause
goto MENU

:START_FRONTEND
cls
echo Starting Frontend Server...
cd /d "%BASE_DIR%\frontend"
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)
set "FRONTEND_DIR=%BASE_DIR%\frontend"
start "Frontend Server - Port 5173" cmd /k "cd /d \"%FRONTEND_DIR%\" && npm run dev"
timeout /t 2 >nul
echo Frontend server started in new window.
echo.
pause
goto MENU

:START_ALL
cls
echo Starting Both Servers...
echo.

echo [1/2] Starting Backend...
cd /d "%BASE_DIR%\backend"
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    call "venv\Scripts\activate.bat"
    pip install -r requirements.txt -q
) else (
    call "venv\Scripts\activate.bat"
)
set "BACKEND_DIR=%BASE_DIR%\backend"
start "Backend Server - Port 8000" cmd /k "cd /d \"%BACKEND_DIR%\" && \"%BACKEND_DIR%\venv\Scripts\activate.bat\" && python main.py"
cd /d "%BASE_DIR%"
timeout /t 2 >nul

echo [2/2] Starting Frontend...
cd /d "%BASE_DIR%\frontend"
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)
set "FRONTEND_DIR=%BASE_DIR%\frontend"
start "Frontend Server - Port 5173" cmd /k "cd /d \"%FRONTEND_DIR%\" && npm run dev"
cd /d "%BASE_DIR%"
timeout /t 2 >nul

echo.
echo ================================================
echo   Both servers started successfully!
echo ================================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo ================================================
echo.
pause
goto MENU

:STOP_BACKEND
cls
echo Stopping Backend Server...
echo.

REM Kill processes on port 8000 and their parent CMD windows
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    set PID=%%a
    REM Get parent process
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        REM Kill parent CMD window if it exists
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    REM Kill the main process
    taskkill /F /PID !PID! >nul 2>&1
    echo Backend server stopped ^(PID: !PID!^)
)

REM Close CMD windows with backend title
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO CSV /NH 2^>nul ^| findstr /I "cmd"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%Backend Server - Port 8000%%'" delete >nul 2>&1
)

REM Kill Python processes running main.py
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul ^| findstr /I "python"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%main.py%%'" delete >nul 2>&1
)

timeout /t 1 >nul
echo Done.
echo.
pause
goto MENU

:STOP_FRONTEND
cls
echo Stopping Frontend Server...
echo.

REM Kill processes on port 5173 and their parent CMD windows
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :5173 ^| findstr LISTENING') do (
    set PID=%%a
    REM Get parent process
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        REM Kill parent CMD window if it exists
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    REM Kill the main process
    taskkill /F /PID !PID! >nul 2>&1
    echo Frontend server stopped ^(PID: !PID!^)
)

REM Close CMD windows with frontend title
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO CSV /NH 2^>nul ^| findstr /I "cmd"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%Frontend Server - Port 5173%%'" delete >nul 2>&1
)

REM Kill node processes related to vite
taskkill /F /IM node.exe /T >nul 2>&1

timeout /t 1 >nul
echo Done.
echo.
pause
goto MENU

:STOP_ALL
cls
echo Stopping All Servers and Closing Windows...
echo.

REM Stop Backend and close its window
echo Stopping Backend...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    set PID=%%a
    REM Get parent process
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        REM Kill parent CMD window if it exists
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    REM Kill the main process
    taskkill /F /PID !PID! >nul 2>&1
    echo   Backend stopped ^(PID: !PID!^)
)

REM Stop Frontend and close its window
echo Stopping Frontend...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :5173 ^| findstr LISTENING') do (
    set PID=%%a
    REM Get parent process
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        REM Kill parent CMD window if it exists
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    REM Kill the main process
    taskkill /F /PID !PID! >nul 2>&1
    echo   Frontend stopped ^(PID: !PID!^)
)

REM Close any remaining CMD windows by title
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO CSV /NH 2^>nul ^| findstr /I "cmd"') do (
    wmic process where "ProcessId=%%a AND ^(CommandLine LIKE '%%Backend Server - Port 8000%%' OR CommandLine LIKE '%%Frontend Server - Port 5173%%'^)" delete >nul 2>&1
)

REM Kill Python processes running main.py
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul ^| findstr /I "python"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%main.py%%'" delete >nul 2>&1
)

REM Kill any remaining node processes
taskkill /F /IM node.exe /T >nul 2>&1

timeout /t 1 >nul
echo.
echo All servers stopped and windows closed.
echo.
pause
goto MENU

:RESTART_BACKEND
cls
echo Restarting Backend Server...
echo.

REM Stop existing backend and close window
echo [1/2] Stopping existing backend...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    set PID=%%a
    REM Get parent process
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        REM Kill parent CMD window if it exists
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    REM Kill the main process
    taskkill /F /PID !PID! >nul 2>&1
)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul ^| findstr /I "python"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%main.py%%'" delete >nul 2>&1
)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO CSV /NH 2^>nul ^| findstr /I "cmd"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%Backend Server - Port 8000%%'" delete >nul 2>&1
)
timeout /t 2 >nul

REM Start backend
echo [2/2] Starting backend...
cd /d "%BASE_DIR%\backend"
if exist "venv\Scripts\python.exe" (
    call "venv\Scripts\activate.bat"
    set "BACKEND_DIR=%BASE_DIR%\backend"
    start "Backend Server - Port 8000" cmd /k "cd /d \"%BACKEND_DIR%\" && \"%BACKEND_DIR%\venv\Scripts\activate.bat\" && python main.py"
    cd /d "%BASE_DIR%"
    timeout /t 2 >nul
    echo Backend server restarted.
) else (
    cd /d "%BASE_DIR%"
    echo Error: Virtual environment not found. Please run "Start Backend Server" first.
)
echo.
pause
goto MENU

:RESTART_FRONTEND
cls
echo Restarting Frontend Server...
echo.

REM Stop existing frontend and close window
echo [1/2] Stopping existing frontend...
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :5173 ^| findstr LISTENING') do (
    set PID=%%a
    REM Get parent process
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        REM Kill parent CMD window if it exists
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    REM Kill the main process
    taskkill /F /PID !PID! >nul 2>&1
)
taskkill /F /IM node.exe /T >nul 2>&1
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO CSV /NH 2^>nul ^| findstr /I "cmd"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%Frontend Server - Port 5173%%'" delete >nul 2>&1
)
timeout /t 2 >nul

REM Start frontend
echo [2/2] Starting frontend...
cd /d "%BASE_DIR%\frontend"
set "FRONTEND_DIR=%BASE_DIR%\frontend"
start "Frontend Server - Port 5173" cmd /k "cd /d \"%FRONTEND_DIR%\" && npm run dev"
cd /d "%BASE_DIR%"
timeout /t 2 >nul
echo Frontend server restarted.
echo.
pause
goto MENU

:RESTART_ALL
cls
echo Restarting All Servers...
echo.

REM Stop all servers and close windows
echo [1/3] Stopping all servers and closing windows...

REM Stop Backend
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    set PID=%%a
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    taskkill /F /PID !PID! >nul 2>&1
)

REM Stop Frontend
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :5173 ^| findstr LISTENING') do (
    set PID=%%a
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    taskkill /F /PID !PID! >nul 2>&1
)

REM Close any remaining CMD windows
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO CSV /NH 2^>nul ^| findstr /I "cmd"') do (
    wmic process where "ProcessId=%%a AND ^(CommandLine LIKE '%%Backend Server - Port 8000%%' OR CommandLine LIKE '%%Frontend Server - Port 5173%%'^)" delete >nul 2>&1
)

for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul ^| findstr /I "python"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%main.py%%'" delete >nul 2>&1
)
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 3 >nul

REM Start backend
echo [2/3] Starting Backend...
cd /d "%BASE_DIR%\backend"
if exist "venv\Scripts\python.exe" (
    call "venv\Scripts\activate.bat"
    set "BACKEND_DIR=%BASE_DIR%\backend"
    start "Backend Server - Port 8000" cmd /k "cd /d \"%BACKEND_DIR%\" && \"%BACKEND_DIR%\venv\Scripts\activate.bat\" && python main.py"
    cd /d "%BASE_DIR%"
    timeout /t 2 >nul
)

REM Start frontend
echo [3/3] Starting Frontend...
cd /d "%BASE_DIR%\frontend"
set "FRONTEND_DIR=%BASE_DIR%\frontend"
start "Frontend Server - Port 5173" cmd /k "cd /d \"%FRONTEND_DIR%\" && npm run dev"
cd /d "%BASE_DIR%"
timeout /t 2 >nul

echo.
echo ================================================
echo   All servers restarted successfully!
echo ================================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo ================================================
echo.
pause
goto MENU

:CHECK_STATUS
cls
echo ================================================
echo   Server Status Check
echo ================================================
echo.

set BACKEND_STATUS=STOPPED
set FRONTEND_STATUS=STOPPED

netstat -aon 2>nul | findstr :8000 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    set BACKEND_STATUS=RUNNING
    for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
        set BACKEND_PID=%%a
    )
)

netstat -aon 2>nul | findstr :5173 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    set FRONTEND_STATUS=RUNNING
    for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :5173 ^| findstr LISTENING') do (
        set FRONTEND_PID=%%a
    )
)

echo Backend Server (Port 8000):
if "!BACKEND_STATUS!"=="RUNNING" (
    echo   Status: RUNNING
    echo   PID: !BACKEND_PID!
    echo   URL: http://localhost:8000
    echo   API Docs: http://localhost:8000/docs
) else (
    echo   Status: STOPPED
)
echo.

echo Frontend Server (Port 5173):
if "!FRONTEND_STATUS!"=="RUNNING" (
    echo   Status: RUNNING
    echo   PID: !FRONTEND_PID!
    echo   URL: http://localhost:5173
) else (
    echo   Status: STOPPED
)
echo.

REM Check if windows are open
tasklist /FI "WINDOWTITLE eq Backend Server - Port 8000*" 2>nul | find /I "cmd.exe" >nul
if %errorlevel% equ 0 (
    echo Backend window: OPEN
) else (
    echo Backend window: CLOSED
)

tasklist /FI "WINDOWTITLE eq Frontend Server - Port 5173*" 2>nul | find /I "cmd.exe" >nul
if %errorlevel% equ 0 (
    echo Frontend window: OPEN
) else (
    echo Frontend window: CLOSED
)

echo.
echo ================================================
echo.
pause
goto MENU

:EXIT
cls
echo Stopping all servers and closing windows before exit...
echo.

REM Stop Backend and close window
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    set PID=%%a
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    taskkill /F /PID !PID! >nul 2>&1
)

REM Stop Frontend and close window
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| findstr :5173 ^| findstr LISTENING') do (
    set PID=%%a
    for /f "tokens=2" %%b in ('wmic process where "ProcessId=!PID!" get ParentProcessId /value 2^>nul ^| findstr "="') do (
        set PARENT_PID=%%b
        set PARENT_PID=!PARENT_PID:ParentProcessId=!
        tasklist /FI "PID eq !PARENT_PID!" /FI "IMAGENAME eq cmd.exe" 2^>nul | find /I "cmd.exe" >nul
        if !errorlevel! equ 0 (
            taskkill /F /PID !PARENT_PID! >nul 2>&1
        )
    )
    taskkill /F /PID !PID! >nul 2>&1
)

REM Close any remaining CMD windows
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO CSV /NH 2^>nul ^| findstr /I "cmd"') do (
    wmic process where "ProcessId=%%a AND ^(CommandLine LIKE '%%Backend Server - Port 8000%%' OR CommandLine LIKE '%%Frontend Server - Port 5173%%'^)" delete >nul 2>&1
)

for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul ^| findstr /I "python"') do (
    wmic process where "ProcessId=%%a AND CommandLine LIKE '%%main.py%%'" delete >nul 2>&1
)
taskkill /F /IM node.exe /T >nul 2>&1

echo All servers stopped and windows closed.
echo Goodbye!
timeout /t 2 >nul
exit /b
