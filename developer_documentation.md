# Mood Tracker Application
## Developer Documentation

### Project Overview
The Mood Tracker is a desktop application built with Python and Tkinter that allows users to record and track their moods over time. The application uses SQLite for data storage, providing persistent mood entries with timestamps.

### Technical Architecture

#### Components
1. **User Interface (UI)**: Built with Tkinter
   - Main window with mood entry field, save button, and listbox
   - Additional buttons for deleting entries and clearing all data
   - Status bar for displaying operation results

2. **Database**: SQLite
   - Single table (`moods`) for storing mood entries
   - Fields: id (primary key), mood_text, timestamp

3. **Application Logic**: Python
   - MoodTrackerApp class handling UI and database operations
   - Event handlers for user interactions

#### File Structure
- `mood_tracker.py`: Main application code
- `mood_tracker.db`: SQLite database (created on first run)
- `mood_tracker.ico`: Application icon

### Implementation Details

#### Database Schema
```sql
CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood_text TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
```

#### Key Functions
- `setup_database()`: Initializes the SQLite database connection and creates the table if it doesn't exist
- `save_mood()`: Saves the current mood entry to the database with a timestamp
- `load_mood_entries()`: Retrieves all mood entries from the database and displays them in the listbox
- `delete_selected()`: Removes the selected entry from the database and updates the display
- `clear_all()`: Deletes all entries from the database after confirmation

### Packaging Instructions

#### PyInstaller Method
The application can be packaged as a standalone executable using PyInstaller. See `windows_packaging_instructions.md` for detailed steps.

#### Pynsist Method
For creating a Windows installer, Pynsist can be used with the provided `installer.cfg` file. See `windows_installer_instructions.md` for detailed steps.

### Testing

#### Database Testing
The core database functionality can be tested using the `test_db_functionality.py` script, which verifies:
- Database connection
- Table creation
- Insert operations
- Retrieve operations
- Delete operations

#### Application Testing
See `testing_instructions.md` for comprehensive testing procedures for both the executable and installer versions.

### Future Enhancements
Potential improvements for future versions:
1. Data visualization (charts/graphs of mood over time)
2. Categories for different types of moods
3. Reminder notifications
4. Data export functionality
5. Cloud synchronization
