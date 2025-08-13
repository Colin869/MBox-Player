import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import json
import threading
import time
from pathlib import Path
from PIL import Image, ImageTk
import pygame
import cv2
from mutagen import File

# VLC availability will be checked when needed
VLC_AVAILABLE = False

class MboxPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mbox Player - Media Center")
        self.root.geometry("1200x800")
        
        # WMC-style colors
        self.bg_color = '#1a1a2e'  # Dark blue background
        self.panel_color = '#16213e'  # Slightly lighter blue for panels
        self.accent_color = '#0f3460'  # Blue accent
        self.text_color = 'white'
        self.highlight_color = '#e94560'  # Red highlight for selection
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        # Media state
        self.current_media = None
        self.is_playing = False
        self.media_list = []
        self.current_index = 0
        self.current_category = "Music"  # Default category
        
        # Create GUI
        self.create_gui()
        self.load_settings()
        
    def create_gui(self):
        # Main container with WMC-style layout
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top navigation bar (WMC style)
        nav_frame = tk.Frame(main_frame, bg=self.panel_color, height=60)
        nav_frame.pack(fill=tk.X, pady=(0, 2))
        nav_frame.pack_propagate(False)
        
        # Back button (WMC style)
        back_btn = tk.Button(nav_frame, text="←", font=('Arial', 16, 'bold'),
                            bg=self.panel_color, fg=self.text_color,
                            relief=tk.FLAT, bd=0, padx=20, pady=10,
                            command=self.go_back)
        back_btn.pack(side=tk.LEFT, padx=10)
        
        # Title (WMC style)
        title_label = tk.Label(nav_frame, text="MBOX PLAYER", 
                              font=('Arial', 20, 'bold'), 
                              fg=self.text_color, bg=self.panel_color)
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Categories (WMC style)
        categories_frame = tk.Frame(content_frame, bg=self.bg_color, width=400)
        categories_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        categories_frame.pack_propagate(False)
        
        # Categories title
        cat_title = tk.Label(categories_frame, text="MEDIA CATEGORIES", 
                            font=('Arial', 16, 'bold'), 
                            fg=self.text_color, bg=self.bg_color)
        cat_title.pack(pady=(0, 20))
        
        # Category buttons (WMC style)
        self.categories = ["Music", "Pictures + Videos", "Extras", "Settings"]
        self.category_buttons = {}
        
        for category in self.categories:
            btn = tk.Button(categories_frame, text=category, 
                           font=('Arial', 14, 'bold'),
                           bg=self.bg_color, fg=self.text_color,
                           relief=tk.FLAT, bd=0, padx=20, pady=15,
                           anchor=tk.W, width=25,
                           command=lambda cat=category: self.select_category(cat))
            btn.pack(fill=tk.X, pady=2)
            self.category_buttons[category] = btn
        
        # Right side - Content area
        self.content_area = tk.Frame(content_frame, bg=self.bg_color)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initialize with Music category
        self.select_category("Music")
        
        # Bottom control bar (WMC style)
        control_frame = tk.Frame(main_frame, bg=self.panel_color, height=80)
        control_frame.pack(fill=tk.X, side=tk.BOTTOM)
        control_frame.pack_propagate(False)
        
        # Control buttons (WMC style)
        controls_inner = tk.Frame(control_frame, bg=self.panel_color)
        controls_inner.pack(expand=True)
        
        # Playlist button
        playlist_btn = tk.Button(controls_inner, text="📋", font=('Arial', 12),
                                bg=self.panel_color, fg=self.text_color,
                                relief=tk.FLAT, bd=0, padx=10, pady=5)
        playlist_btn.pack(side=tk.LEFT, padx=5)
        
        # Volume controls
        vol_minus = tk.Button(controls_inner, text="−", font=('Arial', 12, 'bold'),
                             bg=self.panel_color, fg=self.text_color,
                             relief=tk.FLAT, bd=0, padx=8, pady=5)
        vol_minus.pack(side=tk.LEFT, padx=5)
        
        vol_plus = tk.Button(controls_inner, text="+", font=('Arial', 12, 'bold'),
                            bg=self.panel_color, fg=self.text_color,
                            relief=tk.FLAT, bd=0, padx=8, pady=5)
        vol_plus.pack(side=tk.LEFT, padx=5)
        
        # Playback controls
        stop_btn = tk.Button(controls_inner, text="⏹", font=('Arial', 14),
                            bg=self.panel_color, fg=self.text_color,
                            relief=tk.FLAT, bd=0, padx=10, pady=5,
                            command=self.stop_media)
        stop_btn.pack(side=tk.LEFT, padx=10)
        
        prev_btn = tk.Button(controls_inner, text="⏮", font=('Arial', 14),
                            bg=self.panel_color, fg=self.text_color,
                            relief=tk.FLAT, bd=0, padx=10, pady=5,
                            command=self.previous_track)
        prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.play_button = tk.Button(controls_inner, text="▶", font=('Arial', 18, 'bold'),
                                    bg=self.highlight_color, fg='white',
                                    relief=tk.FLAT, bd=0, padx=15, pady=5,
                                    command=self.play_pause)
        self.play_button.pack(side=tk.LEFT, padx=10)
        
        next_btn = tk.Button(controls_inner, text="⏭", font=('Arial', 14),
                            bg=self.panel_color, fg=self.text_color,
                            relief=tk.FLAT, bd=0, padx=10, pady=5,
                            command=self.next_track)
        next_btn.pack(side=tk.LEFT, padx=5)
        
        # Volume slider
        self.volume_var = tk.DoubleVar(value=70)
        volume_scale = tk.Scale(controls_inner, from_=0, to=100, 
                               orient=tk.HORIZONTAL, 
                               variable=self.volume_var,
                               bg=self.panel_color, fg=self.text_color,
                               highlightbackground=self.panel_color,
                               command=self.set_volume,
                               length=150)
        volume_scale.pack(side=tk.LEFT, padx=20)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W,
                             bg=self.panel_color, fg=self.text_color,
                             font=('Arial', 10))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def select_category(self, category):
        """Switch between media categories"""
        self.current_category = category
        
        # Update button highlights
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(bg=self.highlight_color, fg='white')
            else:
                btn.configure(bg=self.bg_color, fg=self.text_color)
        
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Create category-specific content
        if category == "Music":
            self.create_music_content()
        elif category == "Pictures + Videos":
            self.create_video_content()
        elif category == "Extras":
            self.create_extras_content()
        elif category == "Settings":
            self.create_settings_content()
    
    def create_music_content(self):
        """Create music category content"""
        # Title
        title = tk.Label(self.content_area, text="MUSIC LIBRARY", 
                        font=('Arial', 18, 'bold'), 
                        fg=self.text_color, bg=self.bg_color)
        title.pack(pady=(0, 20))
        
        # Add music button
        add_btn = tk.Button(self.content_area, text="Add Music Files", 
                           font=('Arial', 12, 'bold'),
                           bg=self.highlight_color, fg='white',
                           relief=tk.FLAT, padx=20, pady=10,
                           command=self.add_media)
        add_btn.pack(pady=10)
        
        # Music list
        list_frame = tk.Frame(self.content_area, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.media_listbox = tk.Listbox(list_frame, bg=self.panel_color, fg=self.text_color,
                                       selectbackground=self.highlight_color, 
                                       selectforeground='white',
                                       font=('Arial', 12), height=15)
        self.media_listbox.pack(fill=tk.BOTH, expand=True)
        self.media_listbox.bind('<Double-Button-1>', self.play_selected)
        
        # Now playing info
        self.now_playing_label = tk.Label(self.content_area, 
                                         text="No music selected", 
                                         font=('Arial', 14), 
                                         fg=self.text_color, bg=self.bg_color)
        self.now_playing_label.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.content_area, 
                                           variable=self.progress_var,
                                           maximum=100, length=400)
        self.progress_bar.pack(pady=5)
    
    def create_video_content(self):
        """Create video category content"""
        # Title
        title = tk.Label(self.content_area, text="PICTURES + VIDEOS", 
                        font=('Arial', 18, 'bold'), 
                        fg=self.text_color, bg=self.bg_color)
        title.pack(pady=(0, 20))
        
        # Video grid (placeholder)
        grid_frame = tk.Frame(self.content_area, bg=self.bg_color)
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Picture library
        pic_frame = tk.Frame(grid_frame, bg=self.panel_color, width=200, height=150)
        pic_frame.pack(side=tk.LEFT, padx=10, pady=10)
        pic_frame.pack_propagate(False)
        
        tk.Label(pic_frame, text="Picture Library", 
                font=('Arial', 12, 'bold'), 
                fg=self.text_color, bg=self.panel_color).pack(pady=20)
        
        # Video library
        vid_frame = tk.Frame(grid_frame, bg=self.panel_color, width=200, height=150)
        vid_frame.pack(side=tk.LEFT, padx=10, pady=10)
        vid_frame.pack_propagate(False)
        
        tk.Label(vid_frame, text="Video Library", 
                font=('Arial', 12, 'bold'), 
                fg=self.text_color, bg=self.panel_color).pack(pady=20)
        
        # Add media button
        add_btn = tk.Button(self.content_area, text="Add Media Files", 
                           font=('Arial', 12, 'bold'),
                           bg=self.highlight_color, fg='white',
                           relief=tk.FLAT, padx=20, pady=10,
                           command=self.add_media)
        add_btn.pack(pady=10)
    
    def create_extras_content(self):
        """Create extras category content"""
        title = tk.Label(self.content_area, text="EXTRAS", 
                        font=('Arial', 18, 'bold'), 
                        fg=self.text_color, bg=self.bg_color)
        title.pack(pady=(0, 20))
        
        # Extras options
        extras = ["Play Favorites", "Media Info", "Equalizer", "Playlists"]
        
        for extra in extras:
            btn = tk.Button(self.content_area, text=extra, 
                           font=('Arial', 14, 'bold'),
                           bg=self.bg_color, fg=self.text_color,
                           relief=tk.FLAT, bd=0, padx=20, pady=15,
                           anchor=tk.W, width=25)
            btn.pack(fill=tk.X, pady=2)
    
    def create_settings_content(self):
        """Create settings category content"""
        title = tk.Label(self.content_area, text="SETTINGS", 
                        font=('Arial', 18, 'bold'), 
                        fg=self.text_color, bg=self.bg_color)
        title.pack(pady=(0, 20))
        
        # Settings options
        settings = ["Audio Settings", "Video Settings", "Interface Settings", "About"]
        
        for setting in settings:
            btn = tk.Button(self.content_area, text=setting, 
                           font=('Arial', 14, 'bold'),
                           bg=self.bg_color, fg=self.text_color,
                           relief=tk.FLAT, bd=0, padx=20, pady=15,
                           anchor=tk.W, width=25)
            btn.pack(fill=tk.X, pady=2)
    
    def go_back(self):
        """Go back to previous screen (placeholder)"""
        messagebox.showinfo("Navigation", "Back button functionality coming soon!")
    
    def add_media(self):
        """Add media files to the library"""
        filetypes = [
            ('Media files', '*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.mp3 *.wav *.flac *.m4a *.ogg'),
            ('Video files', '*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm'),
            ('Audio files', '*.mp3 *.wav *.flac *.m4a *.ogg'),
            ('All files', '*.*')
        ]
        
        files = filedialog.askopenfilenames(
            title="Select media files",
            filetypes=filetypes
        )
        
        for file in files:
            if file not in self.media_list:
                self.media_list.append(file)
                filename = os.path.basename(file)
                self.media_listbox.insert(tk.END, filename)
        
        self.save_settings()
        self.status_var.set(f"Added {len(files)} media files")
    
    def play_selected(self, event=None):
        """Play the selected media file"""
        selection = self.media_listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_media()
    
    def play_media(self):
        """Play the current media file"""
        if not self.media_list:
            return
            
        if self.current_index >= len(self.media_list):
            self.current_index = 0
            
        file_path = self.media_list[self.current_index]
        filename = os.path.basename(file_path)
        
        self.now_playing_label.config(text=f"Now Playing: {filename}")
        self.status_var.set(f"Playing: {filename}")
        
        # Determine media type and play accordingly
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.mp3', '.wav', '.flac', '.m4a', '.ogg']:
            self.play_audio(file_path)
        else:
            self.play_video(file_path)
    
    def play_audio(self, file_path):
        """Play audio file using pygame"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.play_button.config(text="⏸", bg=self.highlight_color)
            self.update_progress()
        except Exception as e:
            messagebox.showerror("Error", f"Could not play audio: {str(e)}")
    
    def play_video(self, file_path):
        """Play video file using VLC"""
        try:
            # Check VLC availability at runtime
            try:
                import vlc
                vlc_available = True
            except:
                vlc_available = False
            
            if vlc_available:
                # VLC implementation would go here
                self.is_playing = True
                self.play_button.config(text="⏸", bg=self.highlight_color)
                self.status_var.set(f"Video playback with VLC (not fully implemented)")
            else:
                # Show a placeholder for video files when VLC is not available
                self.is_playing = True
                self.play_button.config(text="⏸", bg=self.highlight_color)
                self.status_var.set(f"Video playback requires VLC media player to be installed")
                messagebox.showinfo("Video Playback", 
                                  "Video playback requires VLC media player to be installed.\n"
                                  "Please install VLC from https://www.videolan.org/")
        except Exception as e:
            messagebox.showerror("Error", f"Could not play video: {str(e)}")
    
    def play_pause(self):
        """Toggle play/pause"""
        if not self.media_list:
            return
            
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_button.config(text="▶", bg=self.highlight_color)
            self.status_var.set("Paused")
        else:
            if self.current_media is None:
                self.play_media()
            else:
                pygame.mixer.music.unpause()
                self.is_playing = True
                self.play_button.config(text="⏸", bg=self.highlight_color)
                self.status_var.set("Playing")
    
    def stop_media(self):
        """Stop current media playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.current_media = None
        self.play_button.config(text="▶", bg=self.highlight_color)
        self.progress_var.set(0)
        self.status_var.set("Stopped")
    
    def previous_track(self):
        """Play previous track"""
        if self.media_list:
            self.current_index = (self.current_index - 1) % len(self.media_list)
            self.play_media()
    
    def next_track(self):
        """Play next track"""
        if self.media_list:
            self.current_index = (self.current_index + 1) % len(self.media_list)
            self.play_media()
    
    def set_volume(self, value):
        """Set volume level"""
        volume = float(value) / 100.0
        pygame.mixer.music.set_volume(volume)
    
    def update_progress(self):
        """Update progress bar"""
        if self.is_playing and pygame.mixer.music.get_busy():
            # This is a simplified progress update
            # In a full implementation, you'd get actual position/duration
            current_pos = pygame.mixer.music.get_pos() / 1000.0  # Convert to seconds
            # For now, just simulate progress
            progress = (time.time() % 100)  # Simulate 0-100 progress
            self.progress_var.set(progress)
            self.root.after(100, self.update_progress)
    
    def load_settings(self):
        """Load saved settings"""
        try:
            if os.path.exists('mbox_settings.json'):
                with open('mbox_settings.json', 'r') as f:
                    settings = json.load(f)
                    self.media_list = settings.get('media_list', [])
                    self.volume_var.set(settings.get('volume', 70))
                    
                    # Update listbox
                    if hasattr(self, 'media_listbox'):
                        for file_path in self.media_list:
                            filename = os.path.basename(file_path)
                            self.media_listbox.insert(tk.END, filename)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save current settings"""
        try:
            settings = {
                'media_list': self.media_list,
                'volume': self.volume_var.get()
            }
            with open('mbox_settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

def main():
    root = tk.Tk()
    app = MboxPlayer(root)
    
    # Set window icon and make it resizable
    root.resizable(True, True)
    root.minsize(1000, 700)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
