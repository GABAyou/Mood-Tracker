# Mood Tracker Application
## Developer Documentation

### Project Overview
The Mood Tracker is a desktop application built with Python and Tkinter that allows users to record and track their moods over time. The application uses SQLite for data storage, providing persistent mood entries with timestamps. It features a customizable interface with dark/light theme options and word wrap functionality.

### Technical Architecture

#### Components
1. **User Interface (UI)**: Built with Tkinter
   - Main window with mood entry field, save button, and listbox
   - Theme toggle button (sun/moon) for switching between light and dark modes
   - Word wrap toggles for input field and list view
   - Additional buttons for deleting entries and clearing all data
   - Status bar for displaying operation results

2. **Database**: SQLite
   - Single table (`moods`) for storing mood entries
   - Fields: id (primary key), mood_text, timestamp

3. **Configuration Management**: JSON
   - Stores user preferences for theme and word wrap settings
   - Persists settings between application sessions

4. **Application Logic**: Python
   - MoodTrackerApp class handling UI and database operations
   - Event handlers for user interactions
   - Theme management system
   - Word wrap implementation with window resize handling

#### File Structure
- `mood_tracker.py`: Main application code
- `mood_tracker.db`: SQLite database (created on first run)
- `mood_tracker_config.json`: User preferences (created on first run)
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

#### Configuration Schema
```json
{
    "theme": "light|dark",
    "input_word_wrap": true|false,
    "list_word_wrap": true|false
}
```

#### Key Functions
- `setup_database()`: Initializes the SQLite database connection and creates the table if it doesn't exist
- `load_config()`: Loads user preferences from the configuration file or creates default settings
- `save_config()`: Saves user preferences to the configuration file
- `apply_theme()`: Applies the current theme to all UI elements
- `toggle_theme()`: Switches between light and dark themes
- `toggle_input_wrap()`: Toggles word wrap for the input field
- `toggle_list_wrap()`: Toggles word wrap for the list view
- `save_mood()`: Saves the current mood entry to the database with a timestamp
- `load_mood_entries()`: Retrieves all mood entries from the database and displays them in the listbox with word wrap if enabled
- `delete_selected()`: Removes the selected entry from the database and updates the display
- `clear_all()`: Deletes all entries from the database after confirmation

#### Theme Implementation
The application implements two themes:
1. **Light Theme**: Black text on white background
   - Background: #ffffff
   - Foreground: #000000
   - Listbox/Entry backgrounds: #ffffff
   - Button background: #f0f0f0
   - Highlight background: #e0e0e0

2. **Dark Theme**: White text on dark background
   - Background: #2d2d2d
   - Foreground: #ffffff
   - Listbox/Entry backgrounds: #3d3d3d
   - Button background: #444444
   - Highlight background: #555555

The theme is applied to all widgets recursively through the widget hierarchy.

#### Word Wrap Implementation
- **Input Field**: Uses Tkinter's Text widget with `wrap=WORD` option when enabled
- **List View**: Implements custom word wrapping logic that:
  1. Calculates available width based on listbox size
  2. Splits text into words and creates wrapped lines
  3. Inserts each line as a separate entry in the listbox
  4. Adds empty lines as separators between entries
- **Window Resize Handling**: Uses the `<Configure>` event binding to detect window resizes and update word wrapping

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

#### Theme and Word Wrap Testing
The theme and word wrap functionality can be tested using the `test_new_features.py` script, which verifies:
- Configuration saving and loading
- Theme switching
- Word wrap with longer text entries

#### Application Testing
See `testing_instructions.md` for comprehensive testing procedures for both the executable and installer versions.

### Future Enhancements
Potential improvements for future versions:
1. Data visualization (charts/graphs of mood over time)
2. Categories for different types of moods
3. Reminder notifications
4. Data export functionality
5. Cloud synchronization
6. Custom theme creation
7. Additional text formatting options
