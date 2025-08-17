#!/usr/bin/env python3
"""
Setup script for TechStore Assistant.
Helps users install dependencies and configure the environment.
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template."""
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists("env_example.txt"):
        try:
            shutil.copy("env_example.txt", ".env")
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your API keys")
            return True
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def check_directories():
    """Check if required directories exist."""
    required_dirs = ["data", "utils"]
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"❌ Required directory '{directory}' not found")
            return False
    print("✅ All required directories exist")
    return True

def main():
    """Main setup function."""
    print("🛍️ TechStore Assistant - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check directories
    if not check_directories():
        print("❌ Setup failed: Missing required directories")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed: Could not install dependencies")
        return
    
    # Create .env file
    if not create_env_file():
        print("❌ Setup failed: Could not create .env file")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit the .env file with your API keys:")
    print("   - Azure OpenAI API key and endpoint")
    print("   - Pinecone API key and environment")
    print("2. Run the demo: python demo.py")
    print("3. Run the full app: streamlit run app.py")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
