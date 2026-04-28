#!/usr/bin/env python3
"""
AI Title Generator - Setup Wizard GUI
User-friendly configuration interface for YouTube uploader
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import sys
import webbrowser
from pathlib import Path

class SetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube AI Uploader - Setup Wizard")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Style
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Config paths
        self.config_file = "config.json"
        self.client_secret_file = "client_secret.json"
        self.config_data = self.load_config()
        
        # Create wizard
        self.create_wizard()
    
    def create_wizard(self):
        """Create the main wizard interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2196F3', height=80)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="YouTube AI Uploader Setup",
            font=("Arial", 18, "bold"),
            bg='#2196F3',
            fg='white'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Configure your uploader in 3 easy steps",
            font=("Arial", 10),
            bg='#2196F3',
            fg='white'
        )
        subtitle_label.pack(pady=5)
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tab structure
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Video Folder
        self.create_tab1(notebook)
        
        # Tab 2: Google Credentials
        self.create_tab2(notebook)
        
        # Tab 3: Additional Settings
        self.create_tab3(notebook)
        
        # Footer with buttons
        footer_frame = tk.Frame(self.root, bg='#f0f0f0')
        footer_frame.pack(fill=tk.X, padx=20, pady=20)
        
        save_button = tk.Button(
            footer_frame,
            text="✓ Save Configuration",
            command=self.save_config,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = tk.Button(
            footer_frame,
            text="✕ Cancel",
            command=self.root.quit,
            bg='#f44336',
            fg='white',
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def create_tab1(self, notebook):
        """Tab 1: Video Folder Selection"""
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="📁 Video Folder")
        
        frame = tk.Frame(tab1, bg='#f0f0f0')
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title = tk.Label(
            frame,
            text="Step 1: Select Your Video Folder",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0'
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Description
        desc = tk.Label(
            frame,
            text="Choose the folder where your MP4 videos are stored.\nThe uploader will scan this folder for videos to upload.\nThis folder setting is saved and used permanently.",
            font=("Arial", 10),
            bg='#f0f0f0',
            justify=tk.LEFT
        )
        desc.pack(anchor=tk.W, pady=(0, 15))
        
        # Folder path display
        path_label = tk.Label(frame, text="Selected Folder:", font=("Arial", 10, "bold"), bg='#f0f0f0')
        path_label.pack(anchor=tk.W)
        
        self.tab1_path = tk.StringVar(value=self.config_data.get("scan_folder", ""))
        
        path_display = tk.Entry(
            frame,
            textvariable=self.tab1_path,
            font=("Arial", 10),
            state='readonly',
            width=50
        )
        path_display.pack(fill=tk.X, pady=(5, 15))
        
        # Browse button
        browse_button = tk.Button(
            frame,
            text="📂 Browse Folder...",
            command=self.browse_folder,
            bg='#2196F3',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        )
        browse_button.pack(pady=10)
        
        # Info box
        info_frame = tk.Frame(frame, bg='#E3F2FD', relief=tk.SOLID, bd=1)
        info_frame.pack(fill=tk.X, pady=15)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Example: C:\\Videos\\MyContent\n\nContent type is detected from video filenames:\n'gameplay_video.mp4' → Gaming | 'unboxing_phone.mp4' → Unboxing",
            font=("Arial", 9),
            bg='#E3F2FD',
            fg='#1565C0',
            justify=tk.LEFT
        )
        info_text.pack(padx=10, pady=10)
    
    def create_tab2(self, notebook):
        """Tab 2: Google Credentials"""
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="🔐 Google Credentials")
        
        frame = tk.Frame(tab2, bg='#f0f0f0')
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title = tk.Label(
            frame,
            text="Step 2: Google OAuth Credentials",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0'
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Description
        desc = tk.Label(
            frame,
            text="Upload to YouTube requires Google authentication.\nYou need to download your credentials from Google Cloud Console.",
            font=("Arial", 10),
            bg='#f0f0f0',
            justify=tk.LEFT
        )
        desc.pack(anchor=tk.W, pady=(0, 15))
        
        # Credentials status
        status_label = tk.Label(frame, text="Credentials Status:", font=("Arial", 10, "bold"), bg='#f0f0f0')
        status_label.pack(anchor=tk.W)
        
        self.tab2_status = tk.StringVar(value="Not configured" if not os.path.exists(self.client_secret_file) else "✓ Found")
        status_display = tk.Label(
            frame,
            textvariable=self.tab2_status,
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#d32f2f'
        )
        status_display.pack(anchor=tk.W, pady=(5, 15))
        
        # Helper link
        helper_frame = tk.Frame(frame, bg='#FFF3E0', relief=tk.SOLID, bd=1)
        helper_frame.pack(fill=tk.X, pady=15)
        
        helper_label = tk.Label(
            helper_frame,
            text="❓ Don't have credentials? ",
            font=("Arial", 9),
            bg='#FFF3E0'
        )
        helper_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        helper_link = tk.Label(
            helper_frame,
            text="Click here to set up Google Cloud →",
            font=("Arial", 9, "underline"),
            bg='#FFF3E0',
            fg='#0066CC',
            cursor="hand2"
        )
        helper_link.pack(side=tk.LEFT, padx=0, pady=10)
        helper_link.bind("<Button-1>", lambda e: webbrowser.open("https://console.cloud.google.com/"))
        
        # Browse button
        browse_creds_button = tk.Button(
            frame,
            text="📄 Select client_secret.json...",
            command=self.browse_credentials,
            bg='#FF9800',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8
        )
        browse_creds_button.pack(pady=10)
        
        # Instructions
        instructions_frame = tk.Frame(frame, bg='#E8F5E9', relief=tk.SOLID, bd=1)
        instructions_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        
        instructions_text = scrolledtext.ScrolledText(
            instructions_frame,
            height=10,
            font=("Courier", 8),
            bg='#E8F5E9',
            fg='#1B5E20',
            wrap=tk.WORD
        )
        instructions_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        instructions_text.insert(tk.END, """HOW TO GET CREDENTIALS:

1. Go to Google Cloud Console
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the JSON file as 'client_secret.json'
6. Use the 'Select' button above to choose the file

The file will be copied to your project folder.""")
        instructions_text.config(state=tk.DISABLED)
    
    def create_tab3(self, notebook):
        """Tab 3: Additional Settings"""
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="⚙️ Settings")
        
        frame = tk.Frame(tab3, bg='#f0f0f0')
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title = tk.Label(
            frame,
            text="Step 3: Additional Settings",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0'
        )
        title.pack(anchor=tk.W, pady=(0, 10))
        
        # Privacy settings
        privacy_label = tk.Label(frame, text="Video Privacy:", font=("Arial", 10, "bold"), bg='#f0f0f0')
        privacy_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.tab3_privacy = tk.StringVar(value=self.config_data.get("privacyStatus", "public"))
        
        privacy_options = [
            ("🔓 Public - Anyone can find and watch", "public"),
            ("🔒 Unlisted - Only with link", "unlisted"),
            ("🔐 Private - Only you can watch", "private")
        ]
        
        for text, value in privacy_options:
            radio = tk.Radiobutton(
                frame,
                text=text,
                variable=self.tab3_privacy,
                value=value,
                font=("Arial", 10),
                bg='#f0f0f0'
            )
            radio.pack(anchor=tk.W, pady=5)
        
        # AI Settings
        ai_label = tk.Label(frame, text="AI Title Generation:", font=("Arial", 10, "bold"), bg='#f0f0f0')
        ai_label.pack(anchor=tk.W, pady=(20, 5))
        
        self.tab3_use_ollama = tk.BooleanVar(value=self.config_data.get("use_ollama", True))
        
        ai_check = tk.Checkbutton(
            frame,
            text="✓ Enable AI-powered title & description generation (requires Ollama)",
            variable=self.tab3_use_ollama,
            font=("Arial", 10),
            bg='#f0f0f0'
        )
        ai_check.pack(anchor=tk.W, pady=10)
        
        # Info
        info_frame = tk.Frame(frame, bg='#E3F2FD', relief=tk.SOLID, bd=1)
        info_frame.pack(fill=tk.X, pady=15)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Uncheck this to use template-based generation instead",
            font=("Arial", 9),
            bg='#E3F2FD',
            fg='#1565C0'
        )
        info_text.pack(padx=10, pady=10)
    
    def load_config(self):
        """Load existing configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def browse_folder(self):
        """Browse for video folder"""
        folder = filedialog.askdirectory(
            title="Select Video Folder",
            initialdir=self.tab1_path.get() or os.path.expanduser("~")
        )
        if folder:
            self.tab1_path.set(folder)
    
    def browse_credentials(self):
        """Browse for client_secret.json"""
        file = filedialog.askopenfilename(
            title="Select client_secret.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=os.path.expanduser("~")
        )
        if file:
            try:
                # Copy file to project folder
                with open(file, 'r') as f:
                    credentials = json.load(f)
                
                with open(self.client_secret_file, 'w') as f:
                    json.dump(credentials, f, indent=2)
                
                self.tab2_status.set("✓ Credentials configured successfully!")
                messagebox.showinfo(
                    "Success",
                    f"Credentials saved to {self.client_secret_file}"
                )
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON file. Please select a valid client_secret.json")
            except Exception as e:
                messagebox.showerror("Error", f"Error copying file: {str(e)}")
    
    def save_config(self):
        """Save configuration to config.json"""
        if not self.tab1_path.get():
            messagebox.showerror("Error", "Please select a video folder")
            return
        
        if not os.path.exists(self.client_secret_file):
            messagebox.showerror("Error", "Please select your Google credentials (client_secret.json)")
            return
        
        try:
            # Load existing config to preserve categories
            config = self.load_config()
            
            # Update with new values
            config["scan_folder"] = self.tab1_path.get()
            config["privacyStatus"] = self.tab3_privacy.get()
            config["use_ollama"] = self.tab3_use_ollama.get()
            
            # Save config
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            messagebox.showinfo(
                "Success",
                "✓ Configuration saved!\n\n"
                "You're all set. You can now use run-uploader.bat to upload your videos."
            )
            
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")


def main():
    root = tk.Tk()
    app = SetupWizard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
