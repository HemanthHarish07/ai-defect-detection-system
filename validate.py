#!/usr/bin/env python3
"""
Validation script for the Automated Defect Detection System.
Checks all components, dependencies, and file structure.
"""

import os
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()

def check_file(path, description):
    """Check if a file exists."""
    full_path = PROJECT_ROOT / path
    if full_path.exists():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - NOT FOUND: {path}")
        return False

def check_directory(path, description):
    """Check if a directory exists."""
    full_path = PROJECT_ROOT / path
    if full_path.is_dir():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - NOT FOUND: {path}")
        return False

def main():
    print("=" * 60)
    print("Automated Defect Detection System - Validation")
    print("=" * 60)
    
    all_good = True
    
    # Check directories
    print("\n📁 Directory Structure:")
    dirs = [
        ("frontend", "Frontend application"),
        ("backend", "Backend API"),
        ("ai-service", "AI Inference Service"),
        ("docs", "Documentation"),
        (".github/workflows", "CI/CD Workflows"),
    ]
    for dir_path, desc in dirs:
        all_good &= check_directory(dir_path, desc)
    
    # Check root files
    print("\n📄 Root Configuration Files:")
    root_files = [
        ("docker-compose.yml", "Docker Compose"),
        ("README.md", "README"),
        (".env.example", "Environment Example"),
        (".gitignore", "Git Ignore"),
    ]
    for file_path, desc in root_files:
        all_good &= check_file(file_path, desc)
    
    # Check backend files
    print("\n🐍 Backend Files:")
    backend_files = [
        ("backend/main.py", "FastAPI main"),
        ("backend/config.py", "Configuration"),
        ("backend/db.py", "Database"),
        ("backend/models.py", "SQLAlchemy Models"),
        ("backend/schemas.py", "Pydantic Schemas"),
        ("backend/routes/upload.py", "Upload Routes"),
        ("backend/routes/history.py", "History Routes"),
        ("backend/services/predict.py", "Prediction Service"),
        ("backend/services/db_ops.py", "Database Operations"),
        ("backend/Dockerfile", "Backend Dockerfile"),
        ("backend/requirements.txt", "Backend Dependencies"),
    ]
    for file_path, desc in backend_files:
        all_good &= check_file(file_path, desc)
    
    # Check AI service files
    print("\n🤖 AI Service Files:")
    ai_files = [
        ("ai-service/api/main.py", "FastAPI main"),
        ("ai-service/inference/predict.py", "Prediction logic"),
        ("ai-service/training/train.py", "Training script"),
        ("ai-service/Dockerfile", "AI Dockerfile"),
        ("ai-service/requirements.txt", "AI Dependencies"),
    ]
    for file_path, desc in ai_files:
        all_good &= check_file(file_path, desc)
    
    # Check frontend files
    print("\n⚛️ Frontend Files:")
    frontend_files = [
        ("frontend/pages/index.js", "Dashboard page"),
        ("frontend/pages/_app.js", "App wrapper"),
        ("frontend/components/UploadCard.js", "Upload component"),
        ("frontend/components/StatsCard.js", "Stats component"),
        ("frontend/services/api.js", "API client"),
        ("frontend/cypress/e2e/upload.cy.js", "E2E tests"),
        ("frontend/package.json", "Frontend dependencies"),
        ("frontend/Dockerfile", "Frontend Dockerfile"),
        ("frontend/next.config.js", "Next.js config"),
        ("frontend/cypress.config.js", "Cypress config"),
    ]
    for file_path, desc in frontend_files:
        all_good &= check_file(file_path, desc)
    
    # Check documentation
    print("\n📚 Documentation:")
    docs = [
        ("docs/SETUP.md", "Setup guide"),
        ("docs/DEPLOYMENT.md", "Deployment guide"),
        ("docs/TRAINING.md", "Training guide"),
        ("docs/ARCHITECTURE.md", "Architecture"),
        ("docs/API.md", "API docs"),
        ("docs/TROUBLESHOOTING.md", "Troubleshooting"),
        ("docs/QUICKREF.md", "Quick reference"),
        ("docs/CHECKLIST.md", "Deployment checklist"),
    ]
    for file_path, desc in docs:
        all_good &= check_file(file_path, desc)
    
    # Check CI/CD
    print("\n🔄 CI/CD:")
    ci_files = [
        (".github/workflows/ci.yml", "GitHub Actions"),
    ]
    for file_path, desc in ci_files:
        all_good &= check_file(file_path, desc)
    
    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("✅ All components present and ready!")
        print("\nNext steps:")
        print("1. docker-compose up --build")
        print("2. Open http://localhost:3000")
        print("3. Upload an image to test")
        return 0
    else:
        print("❌ Some components are missing!")
        print("\nPlease ensure all files are generated.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
