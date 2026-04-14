# ⚡ QUICK START - 5 Minutes to Running

## Step 1: Get Gemini API Key (2 mins)

Go to: **https://ai.google.dev/**

1. Sign in with Google account
2. Click "Get API Key"
3. Create new project if needed
4. Copy your API key

## Step 2: Setup Project (1 min)

```powershell
# Navigate to project
cd c:\Users\Admin\Desktop\Projects\LLM_Project

# Create .env file
echo GEMINI_API_KEY=paste_your_key_here > .env

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Verify Setup (1 min)

```powershell
python setup_verify.py
```

Should show all ✅

## Step 4: Run Pipeline (1 min)

```powershell
python main.py
```

Expected output:
```
🚀 LLM Career Placement Engine - Complete Pipeline
==============================================================

📊 Step 1: Generating synthetic dataset...
  ✅ Generated 60 resumes
  ✅ Generated 22 jobs

📖 Step 2: Parsing resumes and jobs...
  ✅ Parsed 60 resumes
  ✅ Parsed 22 jobs

🤖 Step 3: Extracting skills using Gemini API...
  [Processing...]

⚡ Step 4: Calculating resume-job matches...
  [Processing...]

💾 Step 5: Storing data in SQLite database...
  ✅ Stored 60 resumes in database
  ✅ Stored 22 jobs in database

📊 Step 6: Generating evaluation report...

📈 EVALUATION RESULTS:
  Average Match Score: ~65%
  ...

✅ PIPELINE COMPLETE!
```

## What Gets Created

After running, you'll have:

```
output/
  └── evaluation_report.json     ← Performance metrics
  └── complete_results.json      ← Full results

data/
  └── placement_engine.db        ← SQLite database
  └── resumes.json               ← Generated resumes
  └── jobs.json                  ← Generated jobs
```

## Check Results

View the evaluation report:
```powershell
# PowerShell
Get-Content output\evaluation_report.json | ConvertFrom-Json | ConvertTo-Json

# Or use Python
python -m json.tool output\evaluation_report.json
```

## 🎓 Next: Study the Code

1. **Read `README.md`** - Full project explanation
2. **Read `VIVA_GUIDE.md`** - Interview preparation
3. **Explore `src/` folder:**
   - `llm_service.py` - Gemini integration
   - `skill_extractor.py` - LLM skill extraction
   - `matching_engine.py` - Core algorithm
   - `database_manager.py` - Data storage

## 🐛 Troubleshooting

**ImportError: No module named 'google'?**
```
pip install -r requirements.txt
```

**SyntaxError in config.py?**
- Ensure Python 3.8+
- Check no special characters in code

**API errors?**
- Verify GEMINI_API_KEY in .env
- Check internet connection
- Verify API key is valid

**Database locked?**
```powershell
Remove-Item data\placement_engine.db
python main.py
```

## 📊 Understanding Output

### evaluation_report.json

```json
{
  "summary": {
    "average_match_score": 65.5         // Overall effectiveness
  },
  "detailed_metrics": {
    "role_analysis": {
      "same_role_avg_score": 78.2,      // Same role should be HIGH
      "different_role_avg_score": 42.1  // Different role should be LOW
    }
  },
  "observations": [
    "System effectively identifies skill gaps"
  ]
}
```

**What it means:**
- If same_role > different_role → Algorithm works! ✅
- Higher average score → More accurate matching

## 🎬 For Viva Demo

When interviewer asks to see it working:

```powershell
# 1. Show structure
ls -r

# 2. Show configuration
type config.py | head -30

# 3. Run pipeline
python main.py

# 4. Show results
type output\evaluation_report.json

# 5. Point out: "See how same-role matches score 78% vs different-role 42%"
```

## 💡 Key Files to Understand

| File | Purpose | Complexity |
|------|---------|-----------|
| `config.py` | Settings & constants | ⭐ Easy |
| `main.py` | Orchestrator | ⭐ Easy |
| `data/resume_generator.py` | Generate test data | ⭐⭐ Medium |
| `src/llm_service.py` | Gemini API | ⭐⭐ Medium |
| `src/matching_engine.py` | Core algorithm | ⭐⭐⭐ Hard |
| `src/database_manager.py` | SQLite ops | ⭐⭐ Medium |

## 📚 Learn More

- **Google Gemini API**: https://ai.google.dev/
- **SQLite Python**: https://docs.python.org/3/library/sqlite3.html
- **Project README**: Read README.md
- **Interview Prep**: Read VIVA_GUIDE.md

## 🎯 Success Criteria

Your pipeline works if:

✅ `python main.py` runs without errors  
✅ `output/evaluation_report.json` is created  
✅ Average score shows ~60-70%  
✅ Same-role matches are higher than different-role  
✅ Database file `data/placement_engine.db` exists  

---

**Total time to running: ~5 minutes⏱️**

You're ready to start! 🚀
