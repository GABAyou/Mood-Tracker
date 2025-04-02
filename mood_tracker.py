import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class MoodTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Tracker")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Set up the database
        self.setup_database()
        
        # Create the UI elements
        self.create_widgets()
        
        # Load existing mood entries
        self.load_mood_entries()
    
    def setup_database(self):
        """Create the SQLite database and table if they don't exist"""
        try:
            self.conn = sqlite3.connect('mood_tracker.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS moods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mood_text TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
    
    def create_widgets(self):
        """Create all the UI widgets"""
        # Frame for input area
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        # Mood entry label and text field
        ttk.Label(input_frame, text="How are you feeling?").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mood_entry = ttk.Entry(input_frame, width=40)
        self.mood_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.mood_entry.focus()
        
        # Save button
        save_button = ttk.Button(input_frame, text="Save", command=self.save_mood)
        save_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Bind Enter key to save_mood function
        self.mood_entry.bind("<Return>", lambda event: self.save_mood())
        
        # Frame for the listbox and scrollbar
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label for the list
        ttk.Label(list_frame, text="Your Mood History:").pack(anchor=tk.W)
        
        # Listbox with scrollbar
        self.mood_listbox = tk.Listbox(list_frame, height=15, width=70)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.mood_listbox.yview)
        self.mood_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Pack the listbox and scrollbar
        self.mood_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame for additional actions
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        # Delete button
        delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Clear all button
        clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def save_mood(self):
        """Save the current mood entry to the database"""
        mood_text = self.mood_entry.get().strip()
        if not mood_text:
            messagebox.showwarning("Empty Entry", "Please enter your mood before saving.")
            return
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Insert into database
            self.cursor.execute("INSERT INTO moods (mood_text, timestamp) VALUES (?, ?)", 
                               (mood_text, timestamp))
            self.conn.commit()
            
            # Clear the entry field
            self.mood_entry.delete(0, tk.END)
            
            # Update the listbox
            self.load_mood_entries()
            
            # Update status
            self.status_var.set(f"Mood saved at {timestamp}")
        except sqlite3.Error as e:
            messagebox.showerror("Save Error", f"Failed to save mood: {e}")
    
    def load_mood_entries(self):
        """Load all mood entries from the database into the listbox"""
        try:
            # Clear the listbox
            self.mood_listbox.delete(0, tk.END)
            
            # Get all entries from the database, ordered by most recent first
            self.cursor.execute("SELECT id, mood_text, timestamp FROM moods ORDER BY timestamp DESC")
            entries = self.cursor.fetchall()
            
            # Add entries to the listbox
            for entry in entries:
                entry_id, mood_text, timestamp = entry
                self.mood_listbox.insert(tk.END, f"{timestamp} - {mood_text}")
                
            # Update status
            self.status_var.set(f"Loaded {len(entries)} mood entries")
        except sqlite3.Error as e:
            messagebox.showerror("Load Error", f"Failed to load mood entries: {e}")
    
    def delete_selected(self):
        """Delete the selected mood entry"""
        try:
            # Get selected index
            selected_index = self.mood_listbox.curselection()
            if not selected_index:
                messagebox.showinfo("No Selection", "Please select an entry to delete.")
                return
            
            # Get the entry from the listbox
            selected_entry = self.mood_listbox.get(selected_index)
            
            # Extract timestamp from the entry (assuming format: "YYYY-MM-DD HH:MM:SS - Mood text")
            timestamp = selected_entry.split(" - ")[0]
            
            # Delete from database
            self.cursor.execute("DELETE FROM moods WHERE timestamp = ?", (timestamp,))
            self.conn.commit()
            
            # Reload entries
            self.load_mood_entries()
            
            # Update status
            self.status_var.set(f"Entry deleted: {selected_entry}")
        except Exception as e:
            messagebox.showerror("Delete Error", f"Failed to delete entry: {e}")
    
    def clear_all(self):
        """Clear all mood entries after confirmation"""
        if messagebox.askyesno("Confirm Clear All", "Are you sure you want to delete ALL mood entries?"):
            try:
                # Delete all entries from the database
                self.cursor.execute("DELETE FROM moods")
                self.conn.commit()
                
                # Clear the listbox
                self.mood_listbox.delete(0, tk.END)
                
                # Update status
                self.status_var.set("All entries cleared")
            except sqlite3.Error as e:
                messagebox.showerror("Clear Error", f"Failed to clear entries: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        if self.conn:
            self.conn.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MoodTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
