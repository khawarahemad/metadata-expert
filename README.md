# Metadata Viewer

A modern, cross-platform Python GUI application for viewing image metadata. Supports all common image formats and displays comprehensive EXIF data, file information, and image properties.

## Features

- 🖼️ **Supports All Image Formats**: JPG, PNG, GIF, BMP, TIFF, WebP, and more
- 📊 **Complete Metadata Display**: View EXIF data, file information, and image properties
- 🎨 **Modern UI**: Clean, professional interface with image preview
- 🖥️ **Cross-Platform**: Works seamlessly on macOS and Windows
- 🔍 **Auto-Detection**: Automatically detects image files in selected directories
- 💾 **File Browser**: Built-in file explorer for easy navigation

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python src/main.py
```

### How to Use

1. **Open an Image**: Click the "Open Image" button or drag-and-drop an image file
2. **Browse Directory**: Use the file browser to navigate and view multiple images
3. **View Metadata**: All metadata is displayed in the right panel including:
   - EXIF data (camera info, GPS, timestamps, etc.)
   - File properties (size, format, dimensions)
   - Color profile information
   - Image dimensions and DPI

## Project Structure

```
metadata-edit/
├── src/
│   ├── main.py              # Main application entry point
│   ├── metadata_viewer.py   # Main GUI window and logic
│   └── metadata_parser.py   # Metadata extraction utilities
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .vscode/
    └── settings.json       # VS Code settings
```

## Requirements

- Python 3.8 or higher
- PyQt6 (GUI framework)
- Pillow (Image processing)
- piexif (EXIF data parsing)

## License

MIT License - Feel free to use and modify as needed.
