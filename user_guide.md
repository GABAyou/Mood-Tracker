# Mood Tracker Application
## User Guide

### Introduction
The Mood Tracker is a simple desktop application that allows you to record and track your moods over time. This application provides an easy-to-use interface for entering your current mood, saving it with a timestamp, and viewing your mood history. It features a customizable interface with dark/light theme options and word wrap functionality.

### Installation

#### Method 1: Using the Executable
1. Download the `MoodTracker.exe` file
2. Double-click the file to run the application directly
3. No installation is required

#### Method 2: Using the Installer
1. Download the Mood Tracker installer
2. Run the installer and follow the on-screen instructions
3. The application will be installed in your Program Files directory
4. A shortcut will be created in your Start menu

### Features

#### Recording Your Mood
1. Launch the Mood Tracker application
2. In the text field at the top, type how you're feeling
3. Click the "Save" button or press Enter
4. Your mood will be saved with the current date and time

#### Viewing Your Mood History
- All your recorded moods are displayed in the list below the input field
- Entries are shown with their timestamp in the format: "YYYY-MM-DD HH:MM:SS - Your mood"
- The most recent entries appear at the top of the list

#### Managing Your Entries
- **Delete Selected**: Select an entry from the list and click "Delete Selected" to remove it
- **Clear All**: Click "Clear All" to delete all mood entries (you'll be asked to confirm)

#### Theme Switching
- Click the theme toggle button (☀️/🌙) in the top-right corner to switch between light and dark modes
- Light mode uses a black-on-white color scheme
- Dark mode uses a white-on-black color scheme
- Your theme preference is remembered between sessions

#### Word Wrap
- **Input Field Word Wrap**: Toggle the "Wrap" checkbox next to the input field to enable/disable word wrap
- **List View Word Wrap**: Toggle the "Wrap" checkbox above the list to enable/disable word wrap for entries
- Word wrap automatically adjusts when you resize the application window
- Your word wrap preferences are remembered between sessions

### Data Storage
- Your mood entries are stored in a SQLite database file named `mood_tracker.db`
- Your application preferences (theme, word wrap settings) are stored in `mood_tracker_config.json`
- These files are created in the same directory as the application
- Your data and preferences persist between application launches

### Troubleshooting

#### Application Won't Start
- Ensure you have sufficient permissions to run the application
- If using the installer version, try running as administrator

#### Missing Entries
- Check that you're running the application from the same location each time
- The database is stored relative to the executable location

#### Theme or Word Wrap Settings Not Saving
- Ensure the application has write permissions to its directory
- If issues persist, you can manually delete the `mood_tracker_config.json` file to reset to defaults

#### Other Issues
- Close and restart the application
- If problems persist, try uninstalling and reinstalling the application

### Uninstallation

#### Executable Version
- Simply delete the `MoodTracker.exe` file
- If you want to remove your data and preferences, also delete the `mood_tracker.db` and `mood_tracker_config.json` files

#### Installer Version
- Uninstall through Windows Control Panel or Settings
- Select "Mood Tracker" from the list of installed programs
- Follow the uninstallation prompts
