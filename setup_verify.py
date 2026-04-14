#!/usr/bin/env python3
"""
Quick setup and verification script
Run this to verify everything is working
"""

import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...", end=" ")
    if sys.version_info >= (3, 8):
        print(f"✅ {sys.version.split()[0]}")
        return True
    else:
        print(f"❌ Need Python 3.8+, got {sys.version}")
        return False

def check_project_structure():
    """Verify all directories exist"""
    print("🔍 Checking project structure...", end=" ")
    
    required_dirs = [
        "data",
        "src", 
        "tests",
        "output"
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            print(f"\n  ❌ Missing directory: {dir_name}")
            all_exist = False
    
    if all_exist:
        print("✅")
        return True
    return False

def check_files():
    """Check for required files"""
    print("🔍 Checking required files...", end=" ")
    
    required_files = [
        "config.py",
        "main.py",
        "requirements.txt",
        "data/resume_generator.py",
        "data/job_generator.py",
        "src/llm_service.py",
        "src/skill_extractor.py",
        "src/matching_engine.py",
        "src/database_manager.py",
        "src/resume_parser.py",
        "src/job_parser.py",
        "tests/evaluate.py",
        "README.md",
        "VIVA_GUIDE.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"\n  ❌ Missing file: {file_path}")
            all_exist = False
    
    if all_exist:
        print("✅")
        return True
    return False

def main():
    print("\n" + "="*60)
    print("🚀 LLM Career Placement Engine - Setup Verification")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version()),
        ("Project Structure", check_project_structure()),
        ("Required Files", check_files())
    ]
    
    all_passed = all(check[1] for check in checks)
    
    print("\n" + "="*60)
    
    if all_passed:
        print("✅ All checks passed!")
        print("\n📝 Next steps:")
        print("  1. Get Gemini API key: https://ai.google.dev/")
        print("  2. Create .env file and add your API key:")
        print("     GEMINI_API_KEY=your_key_here")
        print("  3. Install dependencies:")
        print("     pip install -r requirements.txt")
        print("  4. Run the pipeline:")
        print("     python main.py")
    else:
        print("❌ Some checks failed!")
        print("\n Please fix the above issues and try again.")
        sys.exit(1)
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
