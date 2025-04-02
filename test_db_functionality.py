import sqlite3
from datetime import datetime

def test_database_functionality():
    """Test the core database functionality of the mood tracker app"""
    print("Testing database functionality...")
    
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
    
    # Insert a test mood entry
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO moods (mood_text, timestamp) VALUES (?, ?)", 
                      ("Test mood - feeling good", timestamp))
        conn.commit()
        print(f"✓ Inserted test mood entry at {timestamp}")
    except sqlite3.Error as e:
        print(f"✗ Insert operation failed: {e}")
        return False
    
    # Retrieve all entries
    try:
        cursor.execute("SELECT id, mood_text, timestamp FROM moods ORDER BY timestamp DESC")
        entries = cursor.fetchall()
        print(f"✓ Retrieved {len(entries)} entries from database")
        for entry in entries:
            entry_id, mood_text, timestamp = entry
            print(f"  - ID: {entry_id}, Timestamp: {timestamp}, Mood: {mood_text}")
    except sqlite3.Error as e:
        print(f"✗ Retrieve operation failed: {e}")
        return False
    
    # Delete the test entry
    try:
        cursor.execute("DELETE FROM moods WHERE mood_text = ?", ("Test mood - feeling good",))
        conn.commit()
        print("✓ Deleted test mood entry")
    except sqlite3.Error as e:
        print(f"✗ Delete operation failed: {e}")
        return False
    
    # Verify deletion
    try:
        cursor.execute("SELECT COUNT(*) FROM moods WHERE mood_text = ?", ("Test mood - feeling good",))
        count = cursor.fetchone()[0]
        if count == 0:
            print("✓ Verified deletion successful")
        else:
            print("✗ Deletion verification failed")
            return False
    except sqlite3.Error as e:
        print(f"✗ Verification query failed: {e}")
        return False
    
    # Close the connection
    conn.close()
    print("✓ Database connection closed")
    
    print("All database tests passed successfully!")
    return True

if __name__ == "__main__":
    test_database_functionality()
