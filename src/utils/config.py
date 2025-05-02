"""
Configuration Management

This module handles loading, saving, and accessing application configuration.
"""
import os
import json
import sys
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "appearance": {
        "theme": "dark",
        "transparency": 0.8,
        "font_size": 12
    },
    "hotkeys": {
        "toggle_visibility": "ctrl+shift+i",
        "navigate_tab1": "ctrl+shift+1",
        "navigate_tab2": "ctrl+shift+2",
        "navigate_tab3": "ctrl+shift+3",
        "toggle_speech": "ctrl+shift+l"
    },
    "features": {
        # Will be populated by system check
    },
    "system": {
        "tier": "basic",  # Will be updated by system check
        "first_run": True
    }
}

def get_config_dir():
    """Get the configuration directory path."""
    # Use AppData on Windows
    if sys.platform == "win32":
        config_dir = os.path.join(os.environ["APPDATA"], "InterviewAssistant")
    else:
        # Fallback for other platforms
        config_dir = os.path.expanduser("~/.interview-assistant")
    
    # Create the directory if it doesn't exist
    os.makedirs(config_dir, exist_ok=True)
    
    return config_dir

def get_config_path():
    """Get the full path to the configuration file."""
    return os.path.join(get_config_dir(), "config.json")

def load_config():
    """
    Load the configuration from disk.
    
    Returns:
        dict: The configuration dictionary
    """
    config_path = get_config_path()
    
    # If the config file doesn't exist, create it with defaults
    if not os.path.exists(config_path):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    # Load existing config
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        
        # Merge with defaults to ensure all keys exist
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(config)
        
        return merged_config
    except Exception as e:
        print(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """
    Save the configuration to disk.
    
    Args:
        config (dict): The configuration dictionary
    """
    config_path = get_config_path()
    
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

def get_config():
    """
    Get the current configuration.
    
    Returns:
        dict: The configuration dictionary
    """
    return load_config()

def update_config(updates):
    """
    Update specific configuration values.
    
    Args:
        updates (dict): Dictionary of updates to apply
    """
    config = load_config()
    
    # Apply updates recursively
    def update_recursive(target, source):
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                update_recursive(target[key], value)
            else:
                target[key] = value
    
    update_recursive(config, updates)
    save_config(config)