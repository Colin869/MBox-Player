# Mbox Player Configuration
# This file contains all the customizable settings for the media center

# Theme Colors
THEME = {
    'background': '#1a1a1a',           # Main background color
    'secondary_bg': '#2a2a2a',         # Secondary background color
    'accent': '#00ff88',               # Accent color (green)
    'text': 'white',                   # Text color
    'button_bg': '#444444',            # Button background
    'button_fg': 'white',              # Button text color
    'listbox_bg': '#333333',           # Listbox background
    'listbox_fg': 'white',             # Listbox text color
    'listbox_select_bg': '#00ff88',    # Listbox selection background
    'listbox_select_fg': 'black',      # Listbox selection text
    'progress_bg': '#333333',          # Progress bar background
    'progress_fg': '#00ff88',          # Progress bar foreground
}

# Window Settings
WINDOW = {
    'title': 'Mbox Player - Media Center',
    'default_width': 1200,
    'default_height': 800,
    'min_width': 800,
    'min_height': 600,
    'resizable': True,
}

# Media Settings
MEDIA = {
    'supported_audio': ['.mp3', '.wav', '.flac', '.m4a', '.ogg'],
    'supported_video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'default_volume': 70,
    'auto_play_next': True,
    'remember_position': True,
}

# File Settings
FILES = {
    'settings_file': 'mbox_settings.json',
    'log_file': 'mbox_player.log',
    'temp_dir': 'temp',
}

# Player Settings
PLAYER = {
    'fade_duration': 0.5,              # Fade in/out duration in seconds
    'update_interval': 100,            # Progress update interval in milliseconds
    'show_metadata': True,             # Show media metadata
    'show_visualizer': False,          # Show audio visualizer (future feature)
}

# Library Settings
LIBRARY = {
    'auto_scan': False,                # Auto-scan for media files
    'scan_directories': [],            # Directories to auto-scan
    'exclude_patterns': ['*.tmp', '*.temp'],  # Files to exclude
    'max_recent_files': 50,            # Maximum recent files to remember
}

# Keyboard Shortcuts (future feature)
SHORTCUTS = {
    'play_pause': '<space>',
    'stop': '<Escape>',
    'next': '<Right>',
    'previous': '<Left>',
    'volume_up': '<Up>',
    'volume_down': '<Down>',
    'fullscreen': 'F11',
    'mute': 'M',
}

# Advanced Settings
ADVANCED = {
    'enable_hardware_acceleration': True,
    'use_opengl': False,
    'buffer_size': 4096,
    'sample_rate': 44100,
    'channels': 2,
}

def get_theme_color(color_name):
    """Get a theme color by name"""
    return THEME.get(color_name, '#ffffff')

def get_media_setting(setting_name):
    """Get a media setting by name"""
    return MEDIA.get(setting_name, None)

def get_window_setting(setting_name):
    """Get a window setting by name"""
    return WINDOW.get(setting_name, None)
