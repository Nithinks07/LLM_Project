@echo off
REM Activate virtual environment and start Flask app
echo Activating virtual environment...
call llmenv\Scripts\activate.bat

echo Starting LLM Career Placement Engine web server...
echo.
echo 🚀 Web interface is running at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
