import os

def find_system_font(font_name, extensions=(".ttf", ".otf")):
    """Searches common font directories for the given font name."""
    font_dirs = [
        "C:\\Windows\\Fonts\\",  # Windows
        "/usr/share/fonts/",  # Linux
        "/usr/local/share/fonts/",
        os.path.expanduser("~/.fonts/"),  # User-specific Linux fonts
        "/System/Library/Fonts/",  # macOS
        "/Library/Fonts/",
        os.path.expanduser("~/Library/Fonts/"),
    ]

    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for root, _, files in os.walk(font_dir):
                for file in files:
                    if file.lower().startswith(font_name.lower()) and file.lower().endswith(extensions):
                        return os.path.join(root, file)
    
    return None  # Font not found



print(find_system_font("Arial"))