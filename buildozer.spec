[app]
# (str) Title of your application
title = MyKivyApp

# (str) Package name
package.name = mykivyapp

# (str) Package domain
package.domain = org.example

# (str) Source code directory (make sure this is correct)
source.dir = .

# (list) Source files to include (comma-separated)
source.include_exts = py,png,jpg,kv,atlas

# (str) Main script entry point
source.entry_point = main.py

# (str) Application version
version = 1.0

# (list) Supported orientations
orientation = portrait


# (list) Android permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (list) Package data to include
package_data.include_exts = png, jpg, txt, json, csv

# (str) Icon file (optional)
icon.filename = icon.png

# (str) Presplash screen (optional)
presplash.filename = presplash.png

# (str) Full-screen mode
fullscreen = 1

# (str) Android log level (options: 1, 2, 3, 4, 5)
android.log_level = 1

# (bool) Enable AndroidX
android.enable_androidx = True

# (bool) Indicate if the application should be prespawned (faster startup)
android.prespawn = False

# (list) Gradle dependencies
android.gradle_dependencies = 

[buildozer]
# (str) Command line arguments for the build process
buildozer.log_level = 2

[python]
# (list) Modules required by your app
requirements = python3,kivy,plyer

[android]
# (str) Android API target version
android.api = 31

# (str) NDK version
android.ndk = 23b

# (list) Java classes to add manually
android.add_src = 

# (str) NDK directory
android.ndk_path = 

# (str) Path to the SDK directory
android.sdk_path = 

# (str) Build tool version
android.build_tools_version = 30.0.3

# (list) Local Java classpaths
android.add_jars = 

# (list) Features required by the app
android.features = 

# (str) JVM arguments
android.jvm_args = 

# (str) Additional command-line options
android.extra_args = 

# (list) Architecture support (armeabi-v7a, arm64-v8a, x86_64, etc.)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable multi-touch support
android.multi_touch = True

# (bool) Enable hardware acceleration
android.hardware_acceleration = True

# (list) Additional permissions
android.additional_permissions = 

[toolchain]
# (str) Android toolchain directory
android.toolchain = 

[hostpython]
# (str) Python version used to build the app
hostpython = python3

[dependencies]
# (list) Pip packages required for the app
android.pip = requests

[settings]
# (bool) Whether to enable debugging symbols
debug = False
