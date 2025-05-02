"""
Interview Assistant

A Windows application that provides invisible assistance during job interviews.
The application remains hidden from screen sharing while providing the user
with access to prepared information and AI assistance.
"""
import os
import sys
import keyboard
from overlay.invisible_window import InvisibleWindow

def setup_hotkeys(window):
    """Set up global hotkeys for controlling the application."""
    # Register hotkey for toggling visibility
    keyboard.add_hotkey('ctrl+shift+i', window.toggle_visibility)
    
    # More hotkeys will be added later

def main():
    """Main application entry point."""
    print("Starting Interview Assistant...")
    
    # Create the invisible window
    window = InvisibleWindow()
    
    # Set up global hotkeys
    setup_hotkeys(window)
    
    # Run the application
    window.run()

if __name__ == "__main__":
    # Ensure the current directory is in the Python path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run the main application
    main()