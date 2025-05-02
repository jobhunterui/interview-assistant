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

def print_instructions():
    """Print instructions for using the application."""
    print("\n" + "=" * 60)
    print("INTERVIEW ASSISTANT - USAGE INSTRUCTIONS")
    print("=" * 60)
    print("\nThis application operates in two modes:")
    print("\n1. STEALTH MODE (Default)")
    print("   - Window is visible to you")
    print("   - Window is invisible to screen sharing applications")
    print("   - Green indicator dot shows stealth mode is active")
    print("\n2. HIDDEN MODE")
    print("   - Window is completely invisible (even to you)")
    print("   - Use this when you temporarily don't need the assistant")
    print("   - Red indicator dot will show when you toggle back to visible")
    print("\nHOTKEYS:")
    print("   - Press Ctrl+Shift+I to toggle between stealth and hidden modes")
    print("\nAdditional hotkeys will be added in future updates.\n")
    print("=" * 60 + "\n")

def main():
    """Main application entry point."""
    print("Starting Interview Assistant...")
    
    # Print usage instructions
    print_instructions()
    
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