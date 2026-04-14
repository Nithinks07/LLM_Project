# Web Application Deployment Guide

## Overview

Your LLM Career Matcher system has been upgraded with a professional, production-ready web interface. The application is now fully organized with proper directory structure, modern UI/UX design, and comprehensive functionality.

## How to Run the Web Application

### 1. **Activate Virtual Environment** (Windows PowerShell)
```powershell
cd C:\Users\Admin\Desktop\Projects\LLM_Project
.\llmenv\Scripts\Activate.ps1
```

### 2. **Set Python Path** (Windows PowerShell)
```powershell
$env:PYTHONPATH='C:\Users\Admin\Desktop\Projects\LLM_Project'
```

### 3. **Start Flask Web Server**
```powershell
python web/app.py
```

You should see:
```
======================================================================
🚀 LLM CAREER PLACEMENT ENGINE - WEB SERVER
======================================================================

📱 Web Interface: http://localhost:5000
📊 Dashboard: http://localhost:5000/dashboard
ℹ️  About: http://localhost:5000/about

⏸️  Press Ctrl+C to stop the server
======================================================================
```

### 4. **Access the Web Application**
Open your browser and navigate to:
- **Home Page**: http://localhost:5000/
- **Dashboard**: http://localhost:5000/dashboard
- **About**: http://localhost:5000/about

## Key Features

### 📱 Home Page (`/`)
- **Resume Upload**: Drag-and-drop or click to upload resume
- **Skill Extraction**: AI-powered skill identification
- **Job Matching**: Automatic matching against 22 jobs
- **Results Display**: Ranked jobs with detailed scoring breakdown
- **Score Filtering**: Adjust match score threshold with slider

### 📊 Dashboard (`/dashboard`)
- **Summary Statistics**: Total resumes, jobs, average scores, comparisons
- **Score Distribution**: Histogram of match scores
- **Role Analysis**: Same-role vs. cross-role matching performance
- **Algorithm Breakdown**: Visual representation of scoring components
- **Observations**: Key insights from system analysis

### ℹ️ About (`/about`)
- Project overview and motivation
- How the system works (4-step process)
- Matching algorithm explanation
- Technology stack details
- Key features and capabilities
- Data summary and statistics

## Project Structure

```
web/
├── app.py                          # Flask application (REST API)
├── templates/
│   ├── index.html                  # Home page with upload UI
│   ├── dashboard.html              # Analytics dashboard
│   ├── about.html                  # Project information
│   └── results.html                # Results page
├── static/
│   ├── css/main.css                # Professional styling (800+ lines)
│   ├── js/
│   │   ├── main.js                 # Home page interactivity
│   │   └── dashboard.js            # Chart.js visualization
│   └── img/                        # Image assets
└── uploads/                        # Resume file storage
```

## API Endpoints

### GET Routes (Pages)
- `GET /` - Home page
- `GET /dashboard` - Analytics dashboard
- `GET /about` - About page
- `GET /results` - Results page

### POST/GET Routes (API)
- `POST /api/upload-resume` - Upload and process resume
  - Request: FormData with `resume` file
  - Response: JSON with extracted skills
  
- `POST /api/match-jobs` - Match resume against jobs
  - Request: JSON with `skills` array
  - Response: JSON array of matched jobs with scores
  
- `GET /api/job-details/<index>` - Get specific job details
  - Response: JSON with job information
  
- `GET /api/evaluation-report` - Get system performance metrics
  - Response: JSON with statistics and analysis

## Configuration

### File: `web/app.py`
```python
class Config:
    UPLOAD_FOLDER = 'web/uploads'           # Resume storage
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024   # 20MB max file size
    TEMPLATE_FOLDER = 'web/templates'
    STATIC_FOLDER = 'web/static'
```

### Environment Variables
```bash
PYTHONPATH=C:\Users\Admin\Desktop\Projects\LLM_Project
GEMINI_API_KEY=your_api_key_here  # For LLM features
```

## Dependencies

Key packages (see `requirements.txt` for full list):
- `flask==3.0.2` - Web framework
- `google-generativeai==0.8.6` - LLM API
- `scikit-learn` - ML utilities
- `numpy`, `pandas` - Data processing
- `pypdf` - PDF parsing

## Design Highlights

### Frontend Design
- **Modern Color Scheme**: Blue primary (#2563eb) with secondary colors
- **Responsive Layout**: Mobile-first, works on all screen sizes
- **CSS Variables**: Maintainable theming system
- **Smooth Animations**: Professional transitions and effects
- **Card-Based UI**: Clean, organized information layout

### Code Quality
- **Modular Structure**: Separation of concerns
- **Error Handling**: Comprehensive try-catch with logging
- **Validation**: Input validation for uploads
- **Fallback Logic**: Graceful degradation on errors
- **Comments**: Well-documented code

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `web/app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### Module Import Errors
Ensure PYTHONPATH is set before running:
```powershell
$env:PYTHONPATH='C:\Users\Admin\Desktop\Projects\LLM_Project'
```

### GEMINI_API_KEY Not Set Warning
This warning is expected if you haven't configured the API key. The app still works with fallback behavior.

### File Upload Issues
- Check upload folder exists: `web/uploads/`
- Verify file format is supported: PDF, TXT, DOC, DOCX
- Ensure file size < 20MB

## Performance Notes

- **First Load**: May take a few seconds as LLM services initialize
- **Matching**: Takes 2-5 seconds depending on resume complexity
- **Dashboard**: Loads instantly with cached metrics
- **Concurrent Users**: Designed for 1-5 concurrent users in dev mode
- **Production**: Use WSGI server (Gunicorn) for production deployment

## Notes for Development

### Auto-Reload
Flask is running in debug mode with auto-reload enabled. Changes to Python files will automatically restart the server.

### Debugger PIN
Debug PIN: **994-387-733** (shown in console on startup)

### Logging
Check console output for:
- Request logs (IP, method, path, status)
- Error tracebacks with file/line numbers
- API response times
- File upload progress

## Next Steps

1. **Run the main pipeline** to ensure evaluation data is current:
   ```powershell
   python main.py
   ```

2. **Upload a sample resume** through the web interface

3. **View matching results** and verify scores are reasonable

4. **Check the dashboard** for system metrics and insights

5. **Review the about page** for technical details

## Support & Customization

### To Customize Colors
Edit `web/static/css/main.css`:
```css
:root {
    --primary: #2563eb;          /* Change primary color */
    --success: #10b981;          /* Change success color */
    --warning: #f59e0b;          /* Change warning color */
}
```

### To Add New Routes
Edit `web/app.py`:
```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html')
```

### To Modify Styling
Edit `web/static/css/main.css` (well-organized with sections)

### To Add JavaScript
Create new file in `web/static/js/` and include in template:
```html
<script src="{{ url_for('static', filename='js/new_script.js') }}"></script>
```

## Deployment to Production

When ready to deploy to production:

1. **Disable Debug Mode**:
   ```python
   app.run(debug=False, ...)
   ```

2. **Use WSGI Server** (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 web.app:app
   ```

3. **Set Up Environment Variables**:
   Create `.env` file with production keys

4. **Enable HTTPS**:
   Configure with reverse proxy (Nginx, Apache)

5. **Monitor Logs**:
   Use logging service for error tracking

---

**Development Status**: ✅ Complete and Tested
**Last Updated**: 2024
**Version**: 2.0 (Professional Web Interface)
