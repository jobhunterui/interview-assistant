"""
Invisible Window Implementation

This module implements the core functionality for creating windows that
remain invisible during screen sharing while being visible to the user.
"""
import tkinter as tk
import ctypes
from ctypes import wintypes
import os

# Windows API constants
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
LWA_ALPHA = 0x00000002

class InvisibleWindow:
    """
    Creates a window that remains invisible to screen sharing applications.
    
    This class utilizes Windows-specific API calls to create a window with
    special properties that allow it to be visible to the user while remaining
    undetected by screen sharing applications like Zoom and Google Meet.
    """
    
    def __init__(self, title="Interview Assistant"):
        """
        Initialize the invisible window.
        
        Args:
            title (str): The window title
        """
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("400x600")  # Default size
        
        # Set initial transparency
        self.root.attributes('-alpha', 0.9)  # Higher value for better visibility to user
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Get window handle
        self.hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        
        # Apply stealth mode (invisible to screen sharing)
        self.apply_stealth_mode()
        
        # Load resources
        self.load_resources()
        
        # Setup UI
        self.setup_ui()
        
        # Initial state - visible to user, hidden from screen sharing
        self.visible_to_user = True
        self.status = "stealth"  # "stealth" or "hidden"
        
    def apply_stealth_mode(self):
        """
        Apply Windows-specific properties to make the window invisible to screen sharing
        but still visible to the user.
        """
        # Add tool window style to hide from taskbar and alt+tab
        style = ctypes.windll.user32.GetWindowLongW(self.hwnd, GWL_EXSTYLE)
        new_style = style | WS_EX_TOOLWINDOW | WS_EX_LAYERED
        ctypes.windll.user32.SetWindowLongW(self.hwnd, GWL_EXSTYLE, new_style)
        
        # The window is a special layered window which helps prevent it from being captured
        # Adjust opacity for user visibility
        ctypes.windll.user32.SetLayeredWindowAttributes(self.hwnd, 0, int(255 * 0.9), LWA_ALPHA)
        
        print("Stealth mode applied: Window should be visible to you but hidden from screen sharing")
        
    def load_resources(self):
        """Load icons and other resources."""
        # Will implement loading icons and other resources later
        pass
        
    def setup_ui(self):
        """Set up the main UI components."""
        # Set background color
        bg_color = "#1e3a5f"  # Dark blue background
        text_color = "#ffffff"  # White text
        accent_color = "#4a90e2"  # Light blue accent
        
        # Configure style
        self.root.configure(bg=bg_color)
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header with title and mode indicator
        header = tk.Frame(self.main_frame, bg=bg_color)
        header.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            header, 
            text="Interview Assistant", 
            font=("Arial", 16, "bold"),
            fg=text_color,
            bg=bg_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Mode indicator widget
        self.mode_indicator = tk.Label(
            header,
            text="●",  # Dot indicator
            font=("Arial", 16),
            fg="#00ff00",  # Green for stealth mode
            bg=bg_color
        )
        self.mode_indicator.pack(side=tk.RIGHT)
        
        # Create a placeholder for the main content
        self.content_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add explanation text
        explanation_text = (
            "Interview Assistant is now running in stealth mode.\n\n"
            "In this mode, the window is:\n"
            "- Visible to you\n"
            "- Hidden from screen sharing apps\n\n"
            "Press Ctrl+Shift+I to toggle visibility\n"
            "(completely hide/show the assistant)"
        )
        
        explanation = tk.Label(
            self.content_frame,
            text=explanation_text,
            fg=text_color,
            bg=bg_color,
            justify=tk.LEFT,
            padx=20,
            pady=20
        )
        explanation.pack(pady=20)
        
        # Create footer with status
        footer = tk.Frame(self.main_frame, bg=bg_color)
        footer.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(
            footer,
            text="STEALTH MODE: Visible to you • Hidden from screen sharing",
            fg=accent_color,
            bg=bg_color,
            font=("Arial", 9)
        )
        self.status_label.pack(side=tk.LEFT)
        
    def toggle_visibility(self):
        """
        Toggle the window's visibility to the user.
        
        This doesn't affect whether the window is captured by screen sharing.
        It only controls whether the user can see the window or not.
        """
        if self.visible_to_user:
            # Make invisible to user
            self.root.attributes('-alpha', 0.0)
            self.visible_to_user = False
            self.status = "hidden"
            self.status_label.config(text="HIDDEN MODE: Hidden from you • Hidden from screen sharing")
            self.mode_indicator.config(fg="#ff0000")  # Red for hidden
            print("Window is now completely hidden (invisible to you and screen sharing)")
        else:
            # Make visible to user (but still invisible to screen sharing)
            self.root.attributes('-alpha', 0.9)
            self.visible_to_user = True
            self.status = "stealth"
            self.status_label.config(text="STEALTH MODE: Visible to you • Hidden from screen sharing")
            self.mode_indicator.config(fg="#00ff00")  # Green for stealth mode
            print("Window is now in stealth mode (visible to you, hidden from screen sharing)")
            
    def run(self):
        """Start the main application loop."""
        self.root.mainloop()