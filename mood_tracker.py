import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import json
import os

class MoodTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Tracker")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Theme settings
        self.light_theme = {
            'bg': '#ffffff',
            'fg': '#000000',
            'listbox_bg': '#ffffff',
            'listbox_fg': '#000000',
            'entry_bg': '#ffffff',
            'entry_fg': '#000000',
            'button_bg': '#f0f0f0',
            'highlight_bg': '#e0e0e0',
            'highlight_fg': '#000000'
        }
        
        self.dark_theme = {
            'bg': '#2d2d2d',
            'fg': '#ffffff',
            'listbox_bg': '#3d3d3d',
            'listbox_fg': '#ffffff',
            'entry_bg': '#3d3d3d',
            'entry_fg': '#ffffff',
            'button_bg': '#444444',
            'highlight_bg': '#555555',
            'highlight_fg': '#ffffff'
        }
        
        # Load user preferences
        self.config_file = 'mood_tracker_config.json'
        self.load_config()
        
        # Set up the database
        self.setup_database()
        
        # Create the UI elements
        self.create_widgets()
        
        # Apply theme
        self.apply_theme()
        
        # Load existing mood entries
        self.load_mood_entries()
    
    def load_config(self):
        """Load user configuration from file"""
        self.config = {
            'theme': 'light',  # Default theme
            'input_word_wrap': True,  # Default word wrap for input
            'list_word_wrap': True    # Default word wrap for list
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save user configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
    
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
        # Main frame to hold all widgets
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for controls
        top_frame = tk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Theme toggle button
        self.theme_icon_light = "☀️"  # Sun emoji for light mode
        self.theme_icon_dark = "🌙"   # Moon emoji for dark mode
        
        self.theme_button = tk.Button(
            top_frame, 
            text=self.theme_icon_dark if self.config['theme'] == 'light' else self.theme_icon_light,
            command=self.toggle_theme,
            width=2,
            font=('TkDefaultFont', 12)
        )
        self.theme_button.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Frame for input area
        input_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        input_frame.pack(fill=tk.X)
        
        # Mood entry label and text field
        tk.Label(input_frame, text="How are you feeling?").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Word wrap toggle for input
        self.input_wrap_var = tk.BooleanVar(value=self.config['input_word_wrap'])
        self.input_wrap_check = tk.Checkbutton(
            input_frame, 
            text="Wrap", 
            variable=self.input_wrap_var,
            command=self.toggle_input_wrap
        )
        self.input_wrap_check.grid(row=0, column=2, padx=5, pady=5)
        
        # Create a frame for the text entry
        entry_frame = tk.Frame(input_frame)
        entry_frame.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        input_frame.columnconfigure(1, weight=1)
        
        # Use Text widget instead of Entry for word wrap capability
        self.mood_entry = tk.Text(entry_frame, height=1, width=40, wrap=tk.WORD if self.config['input_word_wrap'] else tk.NONE)
        self.mood_entry.pack(fill=tk.X, expand=True)
        self.mood_entry.focus()
        
        # Save button
        save_button = tk.Button(input_frame, text="Save", command=self.save_mood)
        save_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Bind Enter key to save_mood function
        self.mood_entry.bind("<Return>", lambda event: self.save_mood())
        
        # Frame for the listbox and scrollbar
        list_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label for the list and word wrap toggle
        list_header_frame = tk.Frame(list_frame)
        list_header_frame.pack(fill=tk.X)
        
        tk.Label(list_header_frame, text="Your Mood History:").pack(side=tk.LEFT)
        
        # Word wrap toggle for list
        self.list_wrap_var = tk.BooleanVar(value=self.config['list_word_wrap'])
        self.list_wrap_check = tk.Checkbutton(
            list_header_frame, 
            text="Wrap", 
            variable=self.list_wrap_var,
            command=self.toggle_list_wrap
        )
        self.list_wrap_check.pack(side=tk.RIGHT)
        
        # Create a frame for the listbox with scrollbars
        listbox_frame = tk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        # Horizontal scrollbar
        h_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Vertical scrollbar
        v_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox with scrollbars
        self.mood_listbox = tk.Listbox(
            listbox_frame, 
            height=15, 
            width=70,
            xscrollcommand=h_scrollbar.set,
            yscrollcommand=v_scrollbar.set
        )
        
        # Configure scrollbars
        h_scrollbar.config(command=self.mood_listbox.xview)
        v_scrollbar.config(command=self.mood_listbox.yview)
        
        # Pack the listbox
        self.mood_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Button frame for additional actions
        button_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        button_frame.pack(fill=tk.X)
        
        # Delete button
        delete_button = tk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Clear all button
        clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def apply_theme(self):
        """Apply the current theme to all widgets"""
        theme = self.light_theme if self.config['theme'] == 'light' else self.dark_theme
        
        # Update theme button text
        self.theme_button.config(
            text=self.theme_icon_dark if self.config['theme'] == 'light' else self.theme_icon_light
        )
        
        # Apply theme to main window and frames
        self.root.config(bg=theme['bg'])
        self.main_frame.config(bg=theme['bg'])
        
        # Apply to all frames
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=theme['bg'])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.config(bg=theme['bg'])
                        for grandchild in child.winfo_children():
                            self.apply_theme_to_widget(grandchild, theme)
                    else:
                        self.apply_theme_to_widget(child, theme)
            else:
                self.apply_theme_to_widget(widget, theme)
        
        # Apply to status bar
        self.status_bar.config(bg=theme['bg'], fg=theme['fg'])
    
    def apply_theme_to_widget(self, widget, theme):
        """Apply theme to a specific widget based on its type"""
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Checkbutton):
            widget.config(bg=theme['bg'], fg=theme['fg'])
        elif isinstance(widget, tk.Button):
            widget.config(bg=theme['button_bg'], fg=theme['fg'], activebackground=theme['highlight_bg'], activeforeground=theme['highlight_fg'])
        elif isinstance(widget, tk.Listbox):
            widget.config(bg=theme['listbox_bg'], fg=theme['listbox_fg'], selectbackground=theme['highlight_bg'], selectforeground=theme['highlight_fg'])
        elif isinstance(widget, tk.Text):
            widget.config(bg=theme['entry_bg'], fg=theme['entry_fg'], insertbackground=theme['fg'])
        elif isinstance(widget, tk.Scrollbar):
            widget.config(bg=theme['button_bg'], troughcolor=theme['bg'])
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.config['theme'] = 'dark' if self.config['theme'] == 'light' else 'light'
        self.apply_theme()
        self.save_config()
        self.status_var.set(f"Theme changed to {self.config['theme']} mode")
    
    def toggle_input_wrap(self):
        """Toggle word wrap for the input field"""
        self.config['input_word_wrap'] = self.input_wrap_var.get()
        self.mood_entry.config(wrap=tk.WORD if self.config['input_word_wrap'] else tk.NONE)
        self.save_config()
    
    def toggle_list_wrap(self):
        """Toggle word wrap for the listbox"""
        self.config['list_word_wrap'] = self.list_wrap_var.get()
        # Reload entries to apply word wrap setting
        self.load_mood_entries()
        self.save_config()
    
    def save_mood(self):
        """Save the current mood entry to the database"""
        # Get text from the Text widget (from start to end)
        mood_text = self.mood_entry.get("1.0", "end-1c").strip()
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
            self.mood_entry.delete("1.0", tk.END)
            
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
                display_text = f"{timestamp} - {mood_text}"
                
                # Apply word wrap if enabled
                if self.config['list_word_wrap']:
                    # Calculate available width in characters
                    available_width = self.mood_listbox.winfo_width() // 8  # Approximate character width
                    if available_width < 20:  # Default if window not yet sized
                        available_width = 70
                    
                    # Simple word wrap implementation
                    wrapped_lines = []
                    current_line = ""
                    
                    for word in display_text.split():
                        if len(current_line) + len(word) + 1 <= available_width:
                            current_line += (" " + word if current_line else word)
                        else:
                            wrapped_lines.append(current_line)
                            current_line = word
                    
                    if current_line:
                        wrapped_lines.append(current_line)
                    
                    # Insert each wrapped line
                    for line in wrapped_lines:
                        self.mood_listbox.insert(tk.END, line)
                    
                    # Add a separator between entries if there are multiple entries
                    if len(entries) > 1:
                        self.mood_listbox.insert(tk.END, "")
                else:
                    # No word wrap, insert as is
                    self.mood_listbox.insert(tk.END, display_text)
                
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
            
            # If word wrap is enabled, we need to find the actual entry
            if self.config['list_word_wrap']:
                # Get all entries
                self.cursor.execute("SELECT id, mood_text, timestamp FROM moods ORDER BY timestamp DESC")
                entries = self.cursor.fetchall()
                
                # Find which entry this selection belongs to
                current_index = 0
                for entry in entries:
                    entry_id, mood_text, timestamp = entry
                    display_text = f"{timestamp} - {mood_text}"
                    
                    # Calculate how many lines this entry would take
                    available_width = self.mood_listbox.winfo_width() // 8
                    if available_width < 20:
                        available_width = 70
                    
                    lines_count = 1
                    current_line = ""
                    for word in display_text.split():
                        if len(current_line) + len(word) + 1 <= available_width:
                            current_line += (" " + word if current_line else word)
                        else:
                            lines_count += 1
                            current_line = word
                    
                    # Add separator line if not the last entry
                    if len(entries) > 1 and entry != entries[-1]:
                        lines_count += 1
                    
                    # Check if the selected index falls within this entry's lines
                    if selected_index[0] >= current_index and selected_index[0] < current_index + lines_count:
                        # This is the entry to delete
                        self.cursor.execute("DELETE FROM moods WHERE id = ?", (entry_id,))
                        self.conn.commit()
                        self.load_mood_entries()
                        self.status_var.set(f"Entry deleted: {timestamp}")
                        return
                    
                    current_index += lines_count
            else:
                # Extract timestamp from the entry (assuming format: "YYYY-MM-DD HH:MM:SS - Mood text")
                parts = selected_entry.split(" - ", 1)
                if len(parts) >= 2:
                    timestamp = parts[0]
                    
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
    
    # Bind window resize event to update word wrap
    def on_resize(event):
        if hasattr(app, 'config') and app.config['list_word_wrap']:
            # Use after to avoid multiple redraws during resize
            root.after(100, app.load_mood_entries)
    
    root.bind("<Configure>", on_resize)
    
    root.mainloop()

if __name__ == "__main__":
    main()
