"""Setup script for Text-to-SQL Pipeline"""

import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    dirs = ["logs", "data", "outputs"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created directory: {dir_name}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        with open(env_file, "w") as f:
            with open(env_example) as example:
                f.write(example.read())
        print(f"✓ Created .env file from template")
    elif env_file.exists():
        print(f"✓ .env file already exists")
    else:
        print(f"⚠ .env.example not found, skipping .env creation")

def install_requirements():
    """Install Python requirements"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("⚠ requirements.txt not found")
        return False
    
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def test_import():
    """Test basic imports"""
    print("\n🧪 Testing imports...")
    try:
        import langchain
        import streamlit
        import pymysql
        from dotenv import load_dotenv
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("\n1. Configure your environment:")
    print("   - Edit .env file with your database and API credentials")
    print("\n2. Start the web interface:")
    print("   streamlit run app.py")
    print("\n3. Or use the CLI:")
    print("   python cli.py --interactive")
    print("\n4. Or use Python API:")
    print("   from pipeline import create_pipeline")
    print("   pipeline = create_pipeline()")
    print("\n📖 See README.md for more information")
    print("="*60)

def main():
    """Run setup"""
    print("🚀 Text-to-SQL Pipeline Setup")
    print("="*60)
    
    try:
        create_directories()
        create_env_file()
        
        if not install_requirements():
            print("\n⚠ Some dependencies may be missing")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return
        
        if not test_import():
            print("\n⚠ Some imports failed")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return
        
        print_next_steps()
        
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
