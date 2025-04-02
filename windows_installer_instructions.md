# Pynsist Windows Installer Instructions

## Prerequisites
- Windows operating system
- Python 3.10 or later installed
- pip package manager

## Step 1: Set up the environment on Windows
1. Create a folder for the project (e.g., `mood_tracker`)
2. Copy all the provided files into this folder
3. Open Command Prompt as administrator
4. Navigate to the project folder:
   ```
   cd path\to\mood_tracker
   ```
5. Install required packages:
   ```
   pip install pynsist
   ```

## Step 2: Create the installer configuration file
1. Create a file named `installer.cfg` with the following content:
   ```ini
   [Application]
   name=Mood Tracker
   version=1.0
   entry_point=mood_tracker:main
   icon=mood_tracker.ico

   [Python]
   version=3.10.0
   bitness=64

   [Include]
   packages=
       tkinter
       sqlite3
   files=mood_tracker.db
   ```

2. Note: You'll need an icon file (mood_tracker.ico). If you don't have one, you can create or download a simple icon.

## Step 3: Build the installer
1. Run the following command:
   ```
   pynsist installer.cfg
   ```

2. The installer will be created in the `build\nsis` folder

## Step 4: Test the installer
1. Navigate to the `build\nsis` folder
2. Run the installer and follow the prompts
3. Launch the installed application and verify all functionality works correctly

## Notes
- The installer will include Python, so users don't need to install Python separately
- The application will be installed in the Program Files directory by default
- An uninstaller will be created automatically
