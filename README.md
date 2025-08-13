# Mbox Player - Media Center

A modern, customizable media center application inspired by Windows Media Center, built with Python and Tkinter.

## Features

- **Modern Dark Theme**: Sleek dark interface with green accents
- **Media Library Management**: Add, organize, and manage your media files
- **Audio Playback**: Full support for MP3, WAV, FLAC, M4A, and OGG files
- **Video Playback**: Full support for MP4, AVI, MKV, MOV, WMV, FLV, and WebM files (requires VLC)
- **Playback Controls**: Play, pause, stop, previous, next, and volume control
- **Progress Tracking**: Visual progress bar for media playback
- **Settings Persistence**: Your media library and settings are saved automatically
- **Resizable Interface**: Responsive design that adapts to different screen sizes

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

### Getting Started
1. Launch Mbox Player
2. Click "Add Media" to browse and select your media files
3. Double-click any file in the library to start playback
4. Use the control buttons to manage playback

### Controls
- **▶ Play/⏸ Pause**: Toggle playback
- **⏮ Previous**: Play the previous track
- **⏭ Next**: Play the next track
- **⏹ Stop**: Stop current playback
- **Volume Slider**: Adjust playback volume

### Media Library
- **Add Media**: Browse and add media files to your library
- **Clear All**: Remove all media from the library
- **Double-click**: Play any file directly from the library

## Supported Formats

### Audio
- MP3
- WAV
- FLAC
- M4A
- OGG

### Video
- MP4
- AVI
- MKV
- MOV
- WMV
- FLV
- WebM

## File Structure

```
Mbox Player/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── mbox_settings.json  # Saved settings (created automatically)
```

## Customization

The application uses a dark theme with green accents. You can customize the appearance by modifying the color values in `main.py`:

- Background: `#1a1a1a` (dark gray)
- Secondary background: `#2a2a2a` (lighter gray)
- Accent color: `#00ff88` (bright green)
- Text: `white`

## Technical Details

- **GUI Framework**: Tkinter
- **Audio Engine**: Pygame mixer
- **Video Engine**: VLC (planned implementation)
- **Media Metadata**: Mutagen for audio file information
- **Image Processing**: PIL/Pillow for image handling

## Future Enhancements

- [ ] Full video playback integration with VLC
- [ ] Media metadata display (artist, album, duration)
- [ ] Playlist creation and management
- [ ] Equalizer and audio effects
- [ ] Fullscreen mode
- [ ] Keyboard shortcuts
- [ ] Media streaming support
- [ ] Custom themes and skins

## Troubleshooting

### Common Issues

1. **Audio not playing**: Make sure you have the required codecs installed
2. **Video not working**: Video playback is currently limited - audio files work best
3. **Dependencies not found**: Run `pip install -r requirements.txt`

### System Requirements

- Python 3.7 or higher
- Windows 10/11 (tested)
- VLC Media Player (for video playback) - Download from https://www.videolan.org/
- Sufficient RAM for media playback
- Audio output device

## Contributing

Feel free to enhance the Mbox Player by:
- Adding new features
- Improving the UI/UX
- Fixing bugs
- Adding support for more media formats

## License

This project is open source and available under the MIT License.

---

**Enjoy your media with Mbox Player!** 🎵🎬
