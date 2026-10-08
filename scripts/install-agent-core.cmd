@echo off
setlocal
set "INSTALLER=%~dp0install_agent_core.py"

where py >nul 2>nul
if errorlevel 1 goto try_python
py -3 "%INSTALLER%"
if not errorlevel 1 exit /b 0

:try_python
where python >nul 2>nul
if errorlevel 1 goto no_python
python "%INSTALLER%"
exit /b %errorlevel%

:no_python
echo agent-core installer: error: Python 3.10 or newer was not found via py or python. 1>&2
exit /b 1
