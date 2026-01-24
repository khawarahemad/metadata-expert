# 📸 Metadata Expert - Professional Image Metadata Viewer & Editor

> A powerful, modern cross-platform Python GUI application for viewing, editing, and managing image metadata with an intuitive interface supporting Mac and Windows.

[![GitHub](https://img.shields.io/badge/GitHub-metadata--expert-blue?logo=github)](https://github.com/khawarahemad/metadata-expert)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey)]()

## ✨ Features

### 🖼️ **Universal Image Format Support**
- JPG, JPEG, PNG, GIF, BMP, TIFF, WebP, ICO, and more
- Automatic format detection and smart handling
- Works with any standard image file format

### 📊 **Complete Metadata Management**
- **View**: EXIF data, file properties, image dimensions, color profiles
- **Edit**: 40+ editable metadata fields with original value display
- **Export**: Save metadata to text files or create copies
- **Clean**: Remove all metadata for privacy protection

### ✏️ **Advanced Editing Capabilities**
- Edit camera information (make, model, lens)
- Modify date/time stamps and EXIF data
- Update creator info (artist, copyright, description)
- Adjust exposure settings, GPS coordinates, and more
- Auto-backup before any modifications
- Undo support with automatic backups

### **🎨 Modern Professional UI**
- Clean, intuitive PyQt6-based interface
- 🌓 **Dark Mode** toggle (Ctrl+D) for comfortable viewing
- Keyboard shortcuts for quick access (Ctrl+O, Ctrl+E, Ctrl+S)
- Split-panel layout with live preview
- Organized metadata in tabbed interface
- Smart categorization of 40+ metadata fields
- Responsive drag-and-drop support

### **🏷️ Advanced Tagging System**
- Create custom tags for images
- Hierarchical tag organization with categories
- Tag autocomplete from history
- Tag cloud visualization with frequency analysis
- Find images by tags instantly
- Tag statistics and analytics
- Export/import tags in JSON format

### **🗺️ GPS & Location Features**
- Extract GPS coordinates from images
- Visual location display with coordinates
- Reverse geocoding (coordinates to location names)
- Edit GPS coordinates directly
- Remove GPS data for privacy
- Group images by location
- Interactive map URL generation
- GPS altitude extraction and editing

### **🔐 Security & Privacy Features**
- Privacy mode to remove sensitive metadata
- Selective field removal (GPS, timestamps, camera info, personal data)
- Privacy risk reporting
- Metadata encryption support
- Secure file deletion with overwrite
- Batch privacy mode for multiple images
- Sensitive metadata scanning and reporting

### **📱 Advanced Image Operations**
- Batch resize images with aspect ratio control
- Image compression with quality control
- Format conversion (JPG, PNG, WebP, BMP, GIF, TIFF)
- Batch processing for folders
- Create thumbnails automatically
- Get comprehensive image information
- File size optimization reports

### **🔧 Additional Features**
- **Keyboard Shortcuts**: Ctrl+O (Open), Ctrl+E (Edit), Ctrl+S (Export), Ctrl+D (Dark Mode)
- **Advanced Menu**: Access all tools from ⚙️ Advanced button
- **Privacy Report**: Detailed security analysis of image metadata
- **Image Info**: Complete technical specifications
- **GPS Integration**: View and edit location data
- **Responsive Design**: Works smoothly on all screen sizes

### 🔍 **Smart File Management**
- Browse and manage folders of images
- Quick file navigator
- Auto-detect all images in directories
- Batch processing ready
- Responsive and fast performance

### 💾 **Export & Privacy Options**
- Export images to any location
- Save metadata as text files
- Remove EXIF data (privacy mode)
- Create backups automatically
- Restore from backup if needed

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/khawarahemad/metadata-expert.git
   cd metadata-expert
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python main.py
```

Or directly:
```bash
./main.py
```

## 📖 Usage Guide

### Main Interface
1. **📁 Open Image** - Select a single image file to view
2. **📂 Browse Folder** - Load all images from a directory
3. **✏️ Edit Metadata** - Open editor dialog to modify metadata
4. **💾 Export/Save** - Save images and metadata in various formats

### Viewing Metadata
- **Basic Info Tab**: File properties, dimensions, format, size
- **EXIF Data Tab**: Camera settings, timestamps, GPS coordinates
- **Properties Tab**: Color space, transparency, animation info

### Editing Metadata

The edit dialog displays metadata organized by category:
- 📅 Date & Time
- 👤 Creator Info
- 📷 Camera Info
- 🎯 Exposure Settings
- 🔍 Focus & Flash
- 🎨 Image Properties
- 🌍 Location (GPS)
- 📝 Additional Info

**Features**:
- See original values in gray text
- Edit directly in input fields
- Auto-backup before saving
- Clear empty fields option
- Real-time validation

### Export Options

1. **Copy Image** - Save image to new location
2. **Export Metadata** - Save all metadata to `.txt` file
3. **Remove Metadata** - Export image without EXIF data

## 📁 Project Structure

```
metadata-expert/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .github/
│   └── copilot-instructions.md # Development notes
├── .vscode/
│   ├── settings.json           # VS Code settings
│   └── tasks.json              # Build tasks
└── src/
    ├── metadata_viewer.py       # Main GUI application & dialogs
    ├── metadata_parser.py       # Metadata extraction logic
    ├── metadata_editor.py       # Metadata editing & export
    ├── tagging_system.py        # Custom tagging & organization
    ├── gps_handler.py           # GPS & location management
    ├── privacy_handler.py       # Privacy & security features
    └── image_operations.py      # Image processing operations
```
## 📋 Requirements

- Python 3.8+
- PyQt6 (GUI framework)
- Pillow (Image processing)
- piexif (EXIF data handling)

See [requirements.txt](requirements.txt) for exact versions.

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone and enter directory
git clone https://github.com/khawarahemad/metadata-expert.git
cd metadata-expert

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Running Tests

```bash
# Syntax check
python -m py_compile src/*.py

# Run the application
python main.py
```

## 🎯 Use Cases

✅ **Photographers & Content Creators**
- Review and manage photo metadata
- Add copyright and creator information
- Prepare images for publication
- Batch metadata management

✅ **Privacy-Conscious Users**
- Remove location data from photos
- Strip sensitive metadata before sharing
- Verify image privacy settings

✅ **Archivists & Librarians**
- Document image information
- Export metadata for cataloging
- Manage image collections

✅ **Developers**
- Inspect image metadata programmatically
- Test EXIF handling
- Batch process images

## 🐛 Known Limitations

- Some image formats may have limited EXIF support
- Batch editing requires manual file selection
- GPS data editing requires proper EXIF format

## 🔐 Privacy & Security

- No data is sent to external servers
- All processing is local
- Automatic backups before editing
- Optional metadata removal for privacy

## 📝 License

MIT License - Feel free to use, modify, and distribute.

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📧 Contact & Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/khawarahemad/metadata-expert/issues)
- Check existing issues for solutions

## 🎨 Technology Stack

| Component | Technology |
|-----------|-----------|
| GUI Framework | PyQt6 |
| Image Processing | Pillow |
| EXIF Handling | piexif |
| Language | Python 3.8+ |
| Platform | Cross-platform (Mac, Windows, Linux) |

## 📚 Additional Resources

- [EXIF Format Reference](https://en.wikipedia.org/wiki/Exif)
- [Pillow Documentation](https://python-pillow.org/)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [piexif Documentation](https://piexif.readthedocs.io/)

## 🙏 Acknowledgments

Built with:
- PyQt6 for the modern UI
- Pillow for image processing
- piexif for EXIF handling

---

**Made with ❤️ for image enthusiasts everywhere**

⭐ If you find this tool useful, please consider giving it a star on GitHub!

