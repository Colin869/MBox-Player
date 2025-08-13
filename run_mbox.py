#!/usr/bin/env python3
"""
Mbox Player Launcher
A simple launcher script that checks dependencies and starts the media center.
"""

import sys
import subprocess
import importlib.util

def check_dependency(module_name, package_name=None):
    """Check if a Python module is available"""
    if package_name is None:
        package_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ {package_name} is not installed")
        return False
    else:
        print(f"✅ {package_name} is available")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    print("🎵 Mbox Player - Media Center Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    try:
        with open("main.py", "r") as f:
            pass
    except FileNotFoundError:
        print("❌ main.py not found. Please run this script from the Mbox Player directory.")
        return
    
    # Check dependencies
    print("\nChecking dependencies...")
    required_modules = [
        ("tkinter", "tkinter"),
        ("PIL", "Pillow"),
        ("pygame", "pygame"),
        ("cv2", "opencv-python"),
        ("mutagen", "mutagen"),
        ("requests", "requests")
    ]
    
    # Check optional VLC
    try:
        import vlc
        print("✅ python-vlc is available (VLC media player required for video)")
    except ImportError:
        print("⚠️  python-vlc not available (video playback will be limited)")
    except Exception as e:
        print(f"⚠️  VLC not properly configured: {e}")
    
    missing_deps = []
    for module, package in required_modules:
        if not check_dependency(module, package):
            missing_deps.append(package)
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        response = input("Would you like to install them now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            if not install_dependencies():
                print("Please install dependencies manually: pip install -r requirements.txt")
                return
        else:
            print("Please install dependencies manually: pip install -r requirements.txt")
            return
    
    print("\n✅ All dependencies are available!")
    
    # Launch the application
    print("\n🚀 Starting Mbox Player...")
    try:
        import main
        main.main()
    except KeyboardInterrupt:
        print("\n👋 Mbox Player closed by user")
    except Exception as e:
        print(f"\n❌ Error starting Mbox Player: {e}")
        print("Please check the error message above and try again.")

if __name__ == "__main__":
    main()
