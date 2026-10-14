@echo off
echo ============================================================
echo   Compiling and Starting AI Meeting Notes Agent Java Server
echo ============================================================
if not exist bin mkdir bin
javac -d bin src\RAGEngine.java src\MeetingService.java src\MeetingNotesServer.java
if %ERRORLEVEL% EQU 0 (
    echo Compilation successful!
    echo Starting HTTP Server at http://localhost:8080 ...
    echo Press Ctrl+C to stop the server.
    java -cp bin src.MeetingNotesServer
) else (
    echo [ERROR] Java compilation failed. Make sure JDK is installed and in PATH.
    pause
)
