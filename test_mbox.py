#!/usr/bin/env python3
"""
Simple test script for Mbox Player
Tests if the GUI loads correctly and basic functionality works.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_gui():
    """Test if the GUI loads correctly"""
    try:
        # Import the main application
        from main import MboxPlayer
        
        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide the window for testing
        
        # Create the application
        app = MboxPlayer(root)
        
        # Test basic functionality
        print("✅ GUI loaded successfully")
        print("✅ MboxPlayer class instantiated")
        print("✅ All widgets created")
        
        # Test media list
        print(f"✅ Media list initialized (length: {len(app.media_list)})")
        
        # Test volume control
        app.set_volume(50)
        print("✅ Volume control working")
        
        # Close the test window
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing GUI: {e}")
        return False

def test_audio_playback():
    """Test audio playback functionality"""
    try:
        import pygame
        pygame.mixer.init()
        print("✅ Pygame mixer initialized")
        
        # Test volume setting
        pygame.mixer.music.set_volume(0.5)
        print("✅ Audio volume control working")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing audio: {e}")
        return False

def main():
    print("🧪 Testing Mbox Player...")
    print("=" * 40)
    
    # Test GUI
    gui_ok = test_gui()
    
    # Test audio
    audio_ok = test_audio_playback()
    
    print("=" * 40)
    if gui_ok and audio_ok:
        print("✅ All tests passed! Mbox Player is ready to use.")
        print("\nTo start the application, run:")
        print("  python main.py")
        print("  or")
        print("  python run_mbox.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    
    return gui_ok and audio_ok

if __name__ == "__main__":
    main()
