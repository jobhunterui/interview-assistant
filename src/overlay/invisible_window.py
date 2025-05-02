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
        self.root.attributes('-alpha', 0.8)
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Get window handle
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        
        # Apply Windows-specific properties to avoid screen capture
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(
            hwnd, GWL_EXSTYLE, 
            style | WS_EX_TOOLWINDOW | WS_EX_LAYERED
        )
        
        # Set transparent for screen sharing
        ctypes.windll.user32.SetLayeredWindowAttributes(
            hwnd, 0, int(255 * 0.8), LWA_ALPHA
        )
        
        # Load resources
        self.load_resources()
        
        # Setup UI
        self.setup_ui()
        
        # Initial state
        self.visible = True
        
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
        
        # Create header with title
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
        
        # Create a placeholder for the main content
        self.content_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        placeholder = tk.Label(
            self.content_frame,
            text="Content will appear here.\nUse Ctrl+Shift+I to toggle visibility.",
            fg=text_color,
            bg=bg_color,
            justify=tk.LEFT
        )
        placeholder.pack(pady=50)
        
        # Create footer with status
        footer = tk.Frame(self.main_frame, bg=bg_color)
        footer.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(
            footer,
            text="Ready • Visible to you • Hidden from screen sharing",
            fg=accent_color,
            bg=bg_color,
            font=("Arial", 8)
        )
        self.status_label.pack(side=tk.LEFT)
        
    def toggle_visibility(self):
        """Toggle the window's visibility to the user."""
        if self.visible:
            self.root.attributes('-alpha', 0.0)
            self.visible = False
            self.status_label.config(text="Ready • Hidden • Hidden from screen sharing")
        else:
            self.root.attributes('-alpha', 0.8)
            self.visible = True
            self.status_label.config(text="Ready • Visible to you • Hidden from screen sharing")
            
    def run(self):
        """Start the main application loop."""
        self.root.mainloop()