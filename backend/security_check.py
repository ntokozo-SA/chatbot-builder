#!/usr/bin/env python3
"""
Security Check Script for AI Chatbot Builder

This script checks for potential security issues before pushing to GitHub.
Run this before committing to ensure no sensitive data is exposed.
"""

import os
import re
import sys
from pathlib import Path

def check_env_files():
    """Check if .env files exist and contain placeholder values"""
    print("🔍 Checking environment files...")
    
    env_files = [
        "backend/.env",
        "frontend/.env.local", 
        "widget/.env"
    ]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"  ✅ {env_file} exists")
            
            # Check if it contains placeholder values
            with open(env_file, 'r') as f:
                content = f.read()
                
            if "your-" in content or "placeholder" in content:
                print(f"  ⚠️  {env_file} contains placeholder values (safe for GitHub)")
            else:
                print(f"  ❌ {env_file} contains real values - DO NOT COMMIT!")
                return False
        else:
            print(f"  ❌ {env_file} missing - create from env.example")
            return False
    
    return True

def check_gitignore():
    """Check if .env files are properly ignored"""
    print("\n🔍 Checking .gitignore files...")
    
    gitignore_files = [".gitignore", "backend/.gitignore", "frontend/.gitignore", "widget/.gitignore"]
    
    for gitignore in gitignore_files:
        if os.path.exists(gitignore):
            with open(gitignore, 'r') as f:
                content = f.read()
                
            if ".env" in content:
                print(f"  ✅ {gitignore} properly ignores .env files")
            else:
                print(f"  ❌ {gitignore} missing .env ignore rule")
                return False
        else:
            print(f"  ❌ {gitignore} missing")
            return False
    
    return True

def check_hardcoded_secrets():
    """Check for hardcoded secrets in source code"""
    print("\n🔍 Checking for hardcoded secrets...")
    
    # Patterns that might indicate hardcoded secrets
    secret_patterns = [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
        r'key\s*=\s*["\'][^"\']+["\']',
        r'token\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
    ]
    
    # Directories to check
    check_dirs = ["backend/app", "frontend/app", "frontend/components", "widget/src"]
    
    issues_found = []
    
    for check_dir in check_dirs:
        if os.path.exists(check_dir):
            for root, dirs, files in os.walk(check_dir):
                for file in files:
                    if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            for pattern in secret_patterns:
                                matches = re.findall(pattern, content, re.IGNORECASE)
                                for match in matches:
                                    if not any(safe_word in match.lower() for safe_word in ['example', 'placeholder', 'your-']):
                                        issues_found.append(f"{file_path}: {match}")
                        except Exception as e:
                            print(f"  ⚠️  Could not read {file_path}: {e}")
    
    if issues_found:
        print("  ❌ Potential hardcoded secrets found:")
        for issue in issues_found:
            print(f"    - {issue}")
        return False
    else:
        print("  ✅ No hardcoded secrets found")
        return True

def check_database_migrations():
    """Check database migrations for sensitive data"""
    print("\n🔍 Checking database migrations...")
    
    migration_dir = "backend/migrations"
    if os.path.exists(migration_dir):
        for file in os.listdir(migration_dir):
            if file.endswith('.sql'):
                file_path = os.path.join(migration_dir, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Check for potential sensitive data in migrations
                    sensitive_patterns = [
                        r'password\s*=\s*["\'][^"\']+["\']',
                        r'secret\s*=\s*["\'][^"\']+["\']',
                        r'INSERT INTO.*VALUES.*["\'][^"\']+["\']',
                    ]
                    
                    for pattern in sensitive_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            if not any(safe_word in match.lower() for safe_word in ['example', 'test', 'placeholder']):
                                print(f"  ⚠️  Potential sensitive data in {file}: {match[:50]}...")
                                return False
                        
                except Exception as e:
                    print(f"  ⚠️  Could not read {file_path}: {e}")
    
    print("  ✅ Database migrations look safe")
    return True

def main():
    """Run all security checks"""
    print("🔒 Security Check for AI Chatbot Builder")
    print("=" * 50)
    
    checks = [
        check_env_files,
        check_gitignore,
        check_hardcoded_secrets,
        check_database_migrations
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("✅ All security checks passed!")
        print("🚀 Your project is ready for GitHub")
    else:
        print("❌ Security issues found!")
        print("🔧 Please fix the issues above before pushing to GitHub")
        sys.exit(1)

if __name__ == "__main__":
    main() 