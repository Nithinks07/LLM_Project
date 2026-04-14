#!/usr/bin/env python3
# Start Flask development server

import os
from pathlib import Path

# Set environment to development
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'

# Change to project directory
os.chdir(Path(__file__).parent)

# Import and run the app
from app import app

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 LLM Career Placement Engine - Web Server")
    print("="*60)
    print("\n📱 Web Interface: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
