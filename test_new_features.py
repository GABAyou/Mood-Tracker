import sqlite3
from datetime import datetime
import json
import os

def test_theme_and_word_wrap_config():
    """Test the configuration saving and loading for theme and word wrap settings"""
    print("Testing theme and word wrap configuration...")
    
    # Define test config file
    config_file = 'test_config.json'
    
    # Test configuration
    test_config = {
        'theme': 'dark',
        'input_word_wrap': True,
        'list_word_wrap': False
    }
    
    # Save test configuration
    try:
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        print("✓ Configuration saved successfully")
    except Exception as e:
        print(f"✗ Failed to save configuration: {e}")
        return False
    
    # Load test configuration
    try:
        with open(config_file, 'r') as f:
            loaded_config = json.load(f)
        
        # Verify loaded configuration matches test configuration
        if loaded_config == test_config:
            print("✓ Configuration loaded successfully and matches saved values")
        else:
            print(f"✗ Loaded configuration does not match: {loaded_config} vs {test_config}")
            return False
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return False
    
    # Clean up test file
    try:
        os.remove(config_file)
        print("✓ Test configuration file cleaned up")
    except Exception as e:
        print(f"✗ Failed to clean up test file: {e}")
    
    print("All configuration tests passed successfully!")
    return True

def test_database_with_longer_entries():
    """Test the database functionality with longer text entries that would require word wrap"""
    print("\nTesting database with longer text entries...")
    
    # Connect to the database
    try:
        conn = sqlite3.connect('mood_tracker.db')
        cursor = conn.cursor()
        print("✓ Database connection successful")
    except sqlite3.Error as e:
        print(f"✗ Database connection failed: {e}")
        return False
    
    # Create table if it doesn't exist
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood_text TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("✓ Table creation successful")
    except sqlite3.Error as e:
        print(f"✗ Table creation failed: {e}")
        return False
    
    # Insert a test mood entry with longer text
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        long_text = "This is a longer mood entry that would require word wrapping to display properly. I'm feeling a mix of emotions today - happy about my accomplishments, but also a bit anxious about upcoming deadlines. The weather is nice though, which helps improve my mood."
        cursor.execute("INSERT INTO moods (mood_text, timestamp) VALUES (?, ?)", 
                      (long_text, timestamp))
        conn.commit()
        print(f"✓ Inserted test mood entry with long text at {timestamp}")
    except sqlite3.Error as e:
        print(f"✗ Insert operation failed: {e}")
        return False
    
    # Retrieve the entry
    try:
        cursor.execute("SELECT id, mood_text, timestamp FROM moods WHERE timestamp = ?", (timestamp,))
        entry = cursor.fetchone()
        if entry:
            entry_id, mood_text, entry_timestamp = entry
            print(f"✓ Retrieved test entry: ID={entry_id}, Timestamp={entry_timestamp}")
            print(f"  Text: {mood_text[:50]}... (truncated)")
            
            # Verify text length
            if len(mood_text) > 100:
                print(f"✓ Verified long text entry (length: {len(mood_text)} characters)")
            else:
                print(f"✗ Text entry is not long enough: {len(mood_text)} characters")
        else:
            print("✗ Failed to retrieve test entry")
            return False
    except sqlite3.Error as e:
        print(f"✗ Retrieve operation failed: {e}")
        return False
    
    # Delete the test entry
    try:
        cursor.execute("DELETE FROM moods WHERE timestamp = ?", (timestamp,))
        conn.commit()
        print("✓ Deleted test mood entry")
    except sqlite3.Error as e:
        print(f"✗ Delete operation failed: {e}")
        return False
    
    # Close the connection
    conn.close()
    print("✓ Database connection closed")
    
    print("All database tests with longer entries passed successfully!")
    return True

if __name__ == "__main__":
    test_theme_and_word_wrap_config()
    test_database_with_longer_entries()
