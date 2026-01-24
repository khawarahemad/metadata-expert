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
- **Reverse geocoding** with 50+ Indian cities & states support
- Worldwide location database (USA, UK, France, Japan, Australia, etc.)
- Edit GPS coordinates directly
- Remove GPS data for privacy
- Group images by location
- Interactive map URL generation
- GPS altitude extraction and editing
- Automatic location detection for Indian cities and states

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
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies (PyQt6, Pillow, piexif, folium, geopy)
├── README.md                        # Documentation
├── LICENSE                          # MIT License
├── .gitignore                       # Git ignore rules
└── src/
    ├── metadata_viewer.py           # Main GUI application with dialogs
    │                                 # - MetadataViewer: Main window with tabbed interface
    │                                 # - EditMetadataDialog: 40+ editable metadata fields
    │                                 # Features: Dark mode, keyboard shortcuts, advanced menu
    │
    ├── metadata_parser.py           # Metadata extraction & parsing
    │                                 # - EXIF data extraction from all image formats
    │                                 # - MakerNote human-readable parsing (detect camera makers)
    │                                 # - Image properties and file information
    │
    ├── metadata_editor.py           # Metadata editing & export operations
    │                                 # - Edit EXIF data directly
    │                                 # - Export metadata to text files
    │                                 # - Create backups and restore
    │                                 # - Remove EXIF data (privacy mode)
    │
    ├── tagging_system.py            # Custom tagging & image organization
    │                                 # - 318 lines | Hierarchical tag system
    │                                 # - JSON persistence (~/.metadata_expert/tags.json)
    │                                 # - Autocomplete suggestions, tag cloud, statistics
    │
    ├── gps_handler.py               # GPS coordinates & location management
    │                                 # - 290 lines | Coordinate extraction/editing
    │                                 # - Reverse geocoding (60+ locations including 50+ Indian cities)
    │                                 # - Altitude handling, location grouping, map URLs
    │
    ├── privacy_handler.py           # Privacy & security features
    │                                 # - 280 lines | Selective metadata removal
    │                                 # - Category-based privacy (GPS, DateTime, Camera, Personal)
    │                                 # - Risk assessment, encryption, secure deletion
    │
    └── image_operations.py          # Advanced image processing
                                      # - 330 lines | Resize, compress, convert formats
                                      # - Batch processing with statistics
                                      # - Thumbnail generation, quality control
```

### Directory Breakdown

| File/Folder | Purpose | Lines | Status |
|---|---|---|---|
| `main.py` | Entry point - initializes and launches the application | ~10 | ✅ Active |
| `src/metadata_viewer.py` | Main GUI window with 3 tabs, edit dialog, dark mode | ~500+ | ✅ Active |
| `src/metadata_parser.py` | EXIF extraction + MakerNote parsing for camera detection | ~250+ | ✅ Active |
| `src/metadata_editor.py` | EXIF editing, export, backup/restore functionality | ~200+ | ✅ Active |
| `src/tagging_system.py` | Custom tagging with hierarchical organization | 318 | ✅ Active |
| `src/gps_handler.py` | GPS handling + reverse geocoding (60+ locations) | 290 | ✅ Active |
| `src/privacy_handler.py` | Privacy mode, metadata removal, secure deletion | 280 | ✅ Active |
| `src/image_operations.py` | Image resize, compress, convert, batch processing | 330 | ✅ Active |

### Core Dependencies

```
PyQt6 (6.6.1)           - GUI Framework
Pillow (10.1.0)         - Image processing
piexif (1.1.3)          - EXIF data handling
folium (0.14.0)         - Interactive maps (future: map visualization)
geopy (2.3.0)           - Reverse geocoding API support
```

### Configuration & Metadata Storage

- **Tags Database**: `~/.metadata_expert/tags.json` - Persistent tag storage
- **Backups**: Created automatically before metadata edits
- **Cache**: Python bytecode in `.gitignore` (not tracked)
- **IDE Files**: `.vscode/` and `.idea/` in `.gitignore` (not tracked)

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

## 📦 Advanced Modules

The application includes several specialized modules for advanced operations:

### 🏷️ Tagging System (`src/tagging_system.py`)
- Custom metadata tagging with hierarchical organization
- Tag persistence in JSON database (~/.metadata_expert/tags.json)
- Autocomplete suggestions based on frequency
- Tag cloud visualization with statistics
- Batch tagging and tag-based image search

### 🗺️ GPS & Location Handler (`src/gps_handler.py`)
- GPS coordinate extraction and editing in EXIF data
- **Reverse geocoding** with intelligent matching:
  - 50+ Indian cities covering all states
  - Major international cities worldwide
  - Automatic proximity detection (8° radius)
- Altitude extraction and manipulation
- Location-based image grouping by proximity
- Map URL generation for viewing coordinates
- DMS to decimal degree conversion

### 🔐 Privacy & Security Handler (`src/privacy_handler.py`)
- Category-based metadata removal (GPS, timestamps, camera info, personal data)
- Privacy risk assessment with detailed reporting
- Selective metadata removal without full stripping
- Secure file deletion with multi-pass overwriting
- Batch privacy mode for folder operations

### 📱 Image Operations (`src/image_operations.py`)
- Resize images with aspect ratio preservation
- Compress images with quality control (1-100)
- Format conversion between 10+ supported formats
- Batch processing for resize, compress, and convert operations
- Thumbnail generation and image property analysis

### 🖼️ Metadata Parser (`src/metadata_parser.py`)
- **MakerNote human-readable parsing**:
  - Detects camera manufacturers (Apple, Canon, Nikon, Sony, Panasonic, Fujifilm, Olympus)
  - Extracts and displays manufacturer information
  - Converts binary MakerNote data to readable format
- Comprehensive EXIF extraction
- File properties and image information
- Auto-detection of all image formats

### 🎯 Use Cases

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

| Component | Technology | Purpose |
|-----------|-----------|---------|
| GUI Framework | PyQt6 6.6.1 | Cross-platform interface |
| Image Processing | Pillow 10.1.0 | Format handling & operations |
| EXIF Handling | piexif 1.1.3 | Metadata read/write |
| MakerNote Parsing | Custom Parser | Camera manufacturer detection |
| Location Database | LOCATION_DB | 50+ Indian cities & international locations |
| Mapping | folium 0.14.0 | Interactive map visualization |
| Geocoding | geopy 2.3.0 | Reverse geocoding support |
| Language | Python 3.8+ | Core language |
| Platform | Cross-platform | Mac, Windows, Linux |

## 📚 Additional Resources

- [EXIF Format Reference](https://en.wikipedia.org/wiki/Exif)
- [Pillow Documentation](https://python-pillow.org/)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [piexif Documentation](https://piexif.readthedocs.io/)
- [MakerNote Formats](https://www.exiftool.org/)

## 🗺️ Location Database Coverage

### India
- **All Major States**: Covered with state capital coordinates
- **Key Cities**: New Delhi, Mumbai, Chennai, Kolkata, Bangalore, Hyderabad, Pune, Indore, and 40+ more
- **Smart Matching**: Auto-detects nearest city within ~8° radius
- Examples: Delhi, Rajasthan, Tamil Nadu, Maharashtra, Karnataka, Gujarat, Kerala, etc.

### International
- USA: New York, Los Angeles, Chicago, San Francisco, Denver, Seattle
- Europe: London, Paris, Moscow
- Asia: Tokyo, Hong Kong, Singapore
- Australia: Sydney

## 🎯 What's New

### Latest Updates (v2.0)
- ✅ **MakerNote Human-Readable Parsing**: Automatically detects camera manufacturers (Apple, Canon, Nikon, Sony, Panasonic, Fujifilm, Olympus)
- ✅ **Expanded Location Database**: 60+ global locations with focus on Indian cities and states
- ✅ **Smart Geocoding**: Improved proximity matching for better location detection
- ✅ **Complete License**: MIT License included for legal clarity
- ✅ **Documentation**: Comprehensive README with all features and usage guide

## 🙏 Acknowledgments

Built with:
- PyQt6 for the modern UI
- Pillow for image processing
- piexif for EXIF handling
- Community contributions and feedback

---

**Made with ❤️ for image enthusiasts everywhere**

⭐ If you find this tool useful, please consider giving it a star on GitHub!

