[app]
# Application name
title = TubeSaver

# Package name (use your unique identifier, usually reverse domain style)
package.name = tubesaver
package.domain = com.yourname  # Change this to your domain or leave as is

# Package version
version = 1.0

# The entry point of your application
source.include_exts = py,png,jpg,kv,atlas

# Main Python file
source.entrypoint = main.py

# Requirements (libraries needed)
requirements = python3, kivy, kivymd, yt_dlp, threading, requests, plyer

# Presplash and Icon
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

# Orientation (leave it as 'sensor' for automatic rotation)
orientation = portrait

# Fullscreen mode (0 = No, 1 = Yes)
fullscreen = 1

# Enable this if using an internet connection
internet = true

# Permissions required for downloading and saving files
android.permissions = android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE, android.permission.INTERNET, android.permission.FOREGROUND_SERVICE

# Hide the title bar
android.hide_status_bar = True

[buildozer]
# Ignore specific files
ignore_path = .git,__pycache__,assets,docs

[android]
# Target Android API Level
android.api = 31
android.minapi = 21

# Architecture support (arm64-v8a & armeabi-v7a for most Android devices)
android.archs = arm64-v8a, armeabi-v7a

# Package format
android.package_format = apk

# Enable android logcat (for debugging)
log_level = 2

# Enable Java Debugging
android.debug = True
