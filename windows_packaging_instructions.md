# PyInstaller Windows Packaging Instructions

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
   pip install tkinter pyinstaller
   ```

## Step 2: Create the executable
1. Run PyInstaller with the following command:
   ```
   pyinstaller --onefile --windowed --name MoodTracker mood_tracker.py
   ```
   
   Options explained:
   - `--onefile`: Creates a single executable file
   - `--windowed`: Prevents console window from appearing when the application runs
   - `--name MoodTracker`: Names the executable "MoodTracker"

2. The executable will be created in the `dist` folder

## Step 3: Test the executable
1. Navigate to the `dist` folder
2. Run `MoodTracker.exe`
3. Verify all functionality works correctly

## Notes
- The database file will be created in the same directory as the executable
- If you move the executable, the database will be created in the new location
- The first time you run the application, a new empty database will be created
