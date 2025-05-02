"""
System Capability Detection

This module checks the system's hardware and software capabilities
to determine which features can be enabled.
"""
import os
import platform
import psutil

def check_system_capabilities():
    """
    Analyze the system and determine which tier of features to enable.
    
    Returns:
        str: The capability tier ('basic', 'standard', or 'advanced')
    """
    # Get basic system info
    ram_gb = psutil.virtual_memory().total / (1024**3)
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_logical = psutil.cpu_count(logical=True)
    cpu_info = platform.processor()
    
    print(f"System Analysis:")
    print(f"  - RAM: {ram_gb:.2f} GB")
    print(f"  - CPU Cores: {cpu_cores} physical, {cpu_logical} logical")
    print(f"  - Processor: {cpu_info}")
    print(f"  - OS: {platform.system()} {platform.version()}")
    
    # Determine tier based on RAM and CPU
    if ram_gb >= 12 and cpu_cores >= 4:
        tier = "advanced"
    elif ram_gb >= 8 and cpu_cores >= 2:
        tier = "standard"
    else:
        tier = "basic"
    
    print(f"Selected tier: {tier}")
    return tier

def get_feature_set(tier):
    """
    Get the set of enabled features based on the system tier.
    
    Args:
        tier (str): The system capability tier
    
    Returns:
        dict: A dictionary of feature flags
    """
    # Base features available to all tiers
    features = {
        "invisible_window": True,
        "basic_preparation": True,
        "manual_navigation": True,
        "json_storage": True,
    }
    
    # Standard tier features
    if tier in ["standard", "advanced"]:
        features.update({
            "question_matching": True,
            "mid_size_llm": True,
            "hotkey_navigation": True,
        })
    
    # Advanced tier features
    if tier == "advanced":
        features.update({
            "speech_recognition": True,
            "advanced_llm": True,
            "enhanced_ui": True,
        })
    
    return features

if __name__ == "__main__":
    # Test the system check
    tier = check_system_capabilities()
    features = get_feature_set(tier)
    
    print("\nEnabled Features:")
    for feature, enabled in features.items():
        print(f"  - {feature}: {enabled}")