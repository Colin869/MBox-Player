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
        self.root.configure(bg='#1a1a1a')
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        # Media state
        self.current_media = None
        self.is_playing = False
        self.media_list = []
        self.current_index = 0
        
        # Create GUI
        self.create_gui()
        self.load_settings()
        
    def create_gui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="MBOX PLAYER", 
                              font=('Arial', 24, 'bold'), 
                              fg='#00ff88', bg='#1a1a1a')
        title_label.pack(pady=(0, 20))
        
        # Content area
        content_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Media library
        left_panel = tk.Frame(content_frame, bg='#2a2a2a', width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Library controls
        library_frame = tk.Frame(left_panel, bg='#2a2a2a')
        library_frame.pack(fill=tk.X, pady=(10, 5))
        
        tk.Button(library_frame, text="Add Media", 
                 command=self.add_media, 
                 bg='#00ff88', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.FLAT, padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(library_frame, text="Clear All", 
                 command=self.clear_library, 
                 bg='#ff4444', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.FLAT, padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Media list
        list_frame = tk.Frame(left_panel, bg='#2a2a2a')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(list_frame, text="Media Library", 
                font=('Arial', 12, 'bold'), 
                fg='#00ff88', bg='#2a2a2a').pack()
        
        self.media_listbox = tk.Listbox(list_frame, bg='#333333', fg='white',
                                       selectbackground='#00ff88', 
                                       selectforeground='black',
                                       font=('Arial', 10), height=20)
        self.media_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.media_listbox.bind('<Double-Button-1>', self.play_selected)
        
        # Right panel - Player
        right_panel = tk.Frame(content_frame, bg='#2a2a2a')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Now playing info
        self.now_playing_frame = tk.Frame(right_panel, bg='#2a2a2a')
        self.now_playing_frame.pack(fill=tk.X, pady=10)
        
        self.now_playing_label = tk.Label(self.now_playing_frame, 
                                         text="No media selected", 
                                         font=('Arial', 14, 'bold'), 
                                         fg='#00ff88', bg='#2a2a2a')
        self.now_playing_label.pack()
        
        # Video display area
        self.video_frame = tk.Frame(right_panel, bg='#000000', height=400)
        self.video_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.video_frame.pack_propagate(False)
        
        # Controls
        controls_frame = tk.Frame(right_panel, bg='#2a2a2a')
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(controls_frame, 
                                           variable=self.progress_var,
                                           maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
        # Control buttons
        button_frame = tk.Frame(controls_frame, bg='#2a2a2a')
        button_frame.pack(pady=10)
        
        self.play_button = tk.Button(button_frame, text="▶ Play", 
                                    command=self.play_pause, 
                                    bg='#00ff88', fg='black', 
                                    font=('Arial', 12, 'bold'),
                                    relief=tk.FLAT, padx=20, pady=10)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="⏮ Previous", 
                 command=self.previous_track, 
                 bg='#444444', fg='white', 
                 font=('Arial', 12, 'bold'),
                 relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="⏭ Next", 
                 command=self.next_track, 
                 bg='#444444', fg='white', 
                 font=('Arial', 12, 'bold'),
                 relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="⏹ Stop", 
                 command=self.stop_media, 
                 bg='#ff4444', fg='white', 
                 font=('Arial', 12, 'bold'),
                 relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
        
        # Volume control
        volume_frame = tk.Frame(controls_frame, bg='#2a2a2a')
        volume_frame.pack(pady=5)
        
        tk.Label(volume_frame, text="Volume:", 
                font=('Arial', 10), 
                fg='white', bg='#2a2a2a').pack(side=tk.LEFT)
        
        self.volume_var = tk.DoubleVar(value=70)
        self.volume_scale = tk.Scale(volume_frame, from_=0, to=100, 
                                    orient=tk.HORIZONTAL, 
                                    variable=self.volume_var,
                                    bg='#2a2a2a', fg='white',
                                    highlightbackground='#2a2a2a',
                                    command=self.set_volume)
        self.volume_scale.pack(side=tk.LEFT, padx=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W,
                             bg='#333333', fg='#00ff88')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
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
    
    def clear_library(self):
        """Clear all media from the library"""
        if messagebox.askyesno("Clear Library", "Are you sure you want to clear all media?"):
            self.media_list.clear()
            self.media_listbox.delete(0, tk.END)
            self.stop_media()
            self.save_settings()
            self.status_var.set("Library cleared")
    
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
            self.play_button.config(text="⏸ Pause")
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
                self.play_button.config(text="⏸ Pause")
                self.status_var.set(f"Video playback with VLC (not fully implemented)")
            else:
                # Show a placeholder for video files when VLC is not available
                self.is_playing = True
                self.play_button.config(text="⏸ Pause")
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
            self.play_button.config(text="▶ Play")
            self.status_var.set("Paused")
        else:
            if self.current_media is None:
                self.play_media()
            else:
                pygame.mixer.music.unpause()
                self.is_playing = True
                self.play_button.config(text="⏸ Pause")
                self.status_var.set("Playing")
    
    def stop_media(self):
        """Stop current media playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.current_media = None
        self.play_button.config(text="▶ Play")
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
    root.minsize(800, 600)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
