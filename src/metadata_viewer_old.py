"""
Main GUI application for Metadata Viewer.
Modern PyQt6-based interface for viewing image metadata with advanced features.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QPushButton, QFileDialog, QLabel, QScrollArea, QFrame,
    QListWidget, QListWidgetItem, QTabWidget, QDialog, QLineEdit,
    QFormLayout, QMessageBox, QDialogButtonBox, QComboBox, QCheckBox,
    QSpinBox, QDoubleSpinBox, QTextEdit, QMenu
)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QColor, QAction
from PyQt6.QtCore import Qt, QSize, QTimer
from metadata_parser import MetadataParser
from metadata_editor import MetadataEditor
from tagging_system import TaggingSystem
from gps_handler import GPSHandler
from privacy_handler import PrivacyHandler
from image_operations import ImageOperations


class EditMetadataDialog(QDialog):
    """Dialog for editing metadata fields and file timestamps."""
    
    def __init__(self, parent=None, metadata=None, file_path=None):
        super().__init__(parent)
        self.metadata = metadata or {}
        self.file_path = file_path
        self.edited_data = {}
        self.file_timestamp = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        self.setWindowTitle('Edit Image Metadata & File Properties')
        self.setGeometry(50, 50, 950, 950)
        
        main_layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel('ℹ️ Original value shown in gray, edit in the input field - Shows ALL available metadata from image\n🔒 You can also edit File Last Modified time below to make changes untraceable')
        info_font = QFont('System', 10)
        info_font.setItalic(True)
        info_label.setFont(info_font)
        info_label.setStyleSheet("color: #666;")
        main_layout.addWidget(info_label)
        
        # File Timestamp Section
        timestamp_group = QFrame()
        timestamp_group.setStyleSheet("QFrame { border: 1px solid #ddd; border-radius: 5px; padding: 10px; background-color: #f9f9f9; }")
        timestamp_layout = QVBoxLayout(timestamp_group)
        
        timestamp_label = QLabel('⏰ File Last Modified Date & Time (Make Changes Untraceable)')
        timestamp_font = QFont('System', 11)
        timestamp_font.setBold(True)
        timestamp_label.setFont(timestamp_font)
        timestamp_label.setStyleSheet("color: #2c3e50;")
        timestamp_layout.addWidget(timestamp_label)
        
        timestamp_form = QFormLayout()
        timestamp_form.setSpacing(8)
        
        # Get current file timestamp
        if self.file_path:
            from metadata_editor import MetadataEditor
            current_timestamp = MetadataEditor.get_file_timestamp(self.file_path)
        else:
            current_timestamp = ""
        
        current_ts_label = QLabel(f"Current: {current_timestamp}")
        current_ts_label.setStyleSheet("color: #999; font-style: italic;")
        timestamp_form.addRow("Current Timestamp:", current_ts_label)
        
        self.timestamp_input = QLineEdit()
        self.timestamp_input.setText(current_timestamp)
        self.timestamp_input.setPlaceholderText("Format: YYYY-MM-DD HH:MM:SS")
        self.timestamp_input.setMinimumHeight(32)
        self.timestamp_input.setToolTip("Edit to change when the file appears to have been last modified")
        timestamp_form.addRow("New Timestamp:", self.timestamp_input)
        
        timestamp_help = QLabel("Tip: Use the same date/time to match original, or any other date to modify the file timestamp")
        timestamp_help.setStyleSheet("color: #0066cc; font-size: 9px; font-style: italic;")
        timestamp_form.addRow("", timestamp_help)
        
        timestamp_layout.addLayout(timestamp_form)
        main_layout.addWidget(timestamp_group)
        
        # Scrollable area for form
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_widget = QWidget()
        form_layout = QFormLayout(scroll_widget)
        form_layout.setSpacing(5)
        
        # Store all inputs
        self.field_inputs = {}
        self.original_values = {}
        
        # Get metadata
        basic_info = self.metadata.get('Basic Information', {})
        exif_data = self.metadata.get('EXIF Data', {})
        image_props = self.metadata.get('Image Properties', {})
        
        # Combine all metadata
        all_metadata = {**exif_data, **image_props, **basic_info}
        
        # Category mapping for smart organization
        category_keywords = {
            '📅 Date & Time': ['date', 'time', 'datetime', 'timestamp', 'subsec'],
            '👤 Creator Info': ['artist', 'author', 'copyright', 'software', 'description', 'maker', 'rights'],
            '📷 Camera Info': ['make', 'model', 'lens', 'equipment', 'camera', 'serial', 'body'],
            '🎯 Exposure Settings': ['exposure', 'iso', 'shutter', 'aperture', 'f-number', 'metering', 'program', 'mode', 'speed', 'bias'],
            '🔍 Focus & Flash': ['focal', 'flash', 'focus', 'distance', 'af', 'auto'],
            '🎨 Image Properties': ['orientation', 'resolution', 'dpi', 'color', 'saturation', 'contrast', 'brightness', 'white', 'balance', 'compression', 'bits'],
            '� Location': ['gps', 'latitude', 'longitude', 'altitude', 'location', 'coordinate'],
            '📝 Additional Info': ['subject', 'keywords', 'comment', 'unique', 'tag', 'category'],
            '🎬 Media Info': ['duration', 'frame', 'animation', 'loop', 'codec', 'profile'],
        }
        
        # Organize fields by category
        categorized_fields = {cat: [] for cat in category_keywords.keys()}
        categorized_fields['🔧 Other Fields'] = []
        
        # Sort metadata keys into categories
        for key, value in sorted(all_metadata.items()):
            if not value or str(value).strip() == '':
                continue
                
            categorized = False
            key_lower = key.lower()
            
            for category, keywords in category_keywords.items():
                if any(kw in key_lower for kw in keywords):
                    categorized_fields[category].append((key, value))
                    categorized = False
                    break
            
            if not categorized:
                categorized_fields['🔧 Other Fields'].append((key, value))
        
        # Display categorized fields
        for category, fields in categorized_fields.items():
            if not fields:
                continue
            
            # Add category header
            category_label = QLabel(category)
            category_font = QFont('System', 12)
            category_font.setBold(True)
            category_label.setFont(category_font)
            category_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
            form_layout.addRow(category_label, QLabel())
            
            # Add fields
            for field_key, field_value in sorted(fields):
                # Clean up field display name
                display_label = field_key.replace('_', ' ')
                
                # Store original value
                original_str = str(field_value).strip() if field_value else ''
                if not original_str:
                    original_str = '[Not set]'
                
                # Truncate very long values
                display_value = original_str if len(original_str) < 80 else original_str[:77] + '...'
                
                # Create container
                field_container = QWidget()
                field_layout = QVBoxLayout(field_container)
                field_layout.setContentsMargins(0, 0, 0, 0)
                field_layout.setSpacing(2)
                
                # Original value label
                original_label = QLabel(f"Original: {display_value}")
                original_label_font = QFont('System', 9)
                original_label_font.setItalic(True)
                original_label.setFont(original_label_font)
                original_label.setStyleSheet("color: #999;")
                original_label.setWordWrap(True)
                field_layout.addWidget(original_label)
                
                # Input field
                input_field = QLineEdit()
                if field_value:
                    input_field.setText(str(field_value).strip())
                input_field.setMinimumHeight(28)
                input_field.setPlaceholderText(f"Edit {display_label.lower()}")
                self.field_inputs[field_key] = input_field
                field_layout.addWidget(input_field)
                
                # Add to form
                form_layout.addRow(QLabel(display_label), field_container)
            
            # Add spacing
            form_layout.addRow(QLabel(''), QLabel(''))
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton('💾 Save All Changes')
        save_button.clicked.connect(self.save_changes)
        save_button.setMinimumHeight(35)
        save_button.setFont(QFont('System', 11))
        
        clear_button = QPushButton('🔄 Clear Empty Fields')
        clear_button.clicked.connect(self.clear_empty_fields)
        clear_button.setMinimumHeight(35)
        clear_button.setFont(QFont('System', 11))
        
        cancel_button = QPushButton('❌ Cancel')
        cancel_button.clicked.connect(self.reject)
        cancel_button.setMinimumHeight(35)
        cancel_button.setFont(QFont('System', 11))
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)
    
    def clear_empty_fields(self):
        """Clear all empty input fields."""
        for input_field in self.field_inputs.values():
            if not input_field.text().strip():
                input_field.clear()
        QMessageBox.information(self, 'Done', 'Empty fields cleared')
    
    def save_changes(self):
        """Collect edited data and close dialog."""
        for field, input_field in self.field_inputs.items():
            value = input_field.text().strip()
            if value:  # Only save non-empty fields
                self.edited_data[field] = value
        
        # Save file timestamp if modified
        self.file_timestamp = self.timestamp_input.text().strip()
        
        self.accept()
    
    def get_edited_data(self):
        """Return the edited metadata."""
        return self.edited_data
    
    def get_file_timestamp(self):
        """Return the edited file timestamp."""
        return self.file_timestamp


class MetadataViewer(QMainWindow):
    """Main application window for viewing image metadata."""

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.current_directory = Path.home()
        self.image_list = []
        self.current_index = 0
        self.dark_mode = False
        self.tagging_system = TaggingSystem()
        
        self.init_ui()
        self.setWindowTitle('🖼️ Metadata Expert - Professional Image Metadata Manager')
        self.setGeometry(100, 100, 1600, 900)
        self.setWindowIcon(self.create_icon())
        
        # Setup keyboard shortcuts
        self.setup_keyboard_shortcuts()

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts."""
        self.open_shortcut = QAction("Open", self)
        self.open_shortcut.setShortcut("Ctrl+O")
        self.open_shortcut.triggered.connect(self.open_image)
        self.addAction(self.open_shortcut)
        
        self.edit_shortcut = QAction("Edit", self)
        self.edit_shortcut.setShortcut("Ctrl+E")
        self.edit_shortcut.triggered.connect(self.edit_metadata)
        self.addAction(self.edit_shortcut)
        
        self.export_shortcut = QAction("Export", self)
        self.export_shortcut.setShortcut("Ctrl+S")
        self.export_shortcut.triggered.connect(self.export_image)
        self.addAction(self.export_shortcut)
        
        self.dark_mode_shortcut = QAction("Dark Mode", self)
        self.dark_mode_shortcut.setShortcut("Ctrl+D")
        self.dark_mode_shortcut.triggered.connect(self.toggle_dark_mode)
        self.addAction(self.dark_mode_shortcut)

    def toggle_dark_mode(self):
        """Toggle dark/light mode."""
        self.dark_mode = not self.dark_mode
        
        if self.dark_mode:
            self.setStyleSheet(self.get_dark_stylesheet())
            QMessageBox.information(self, "Dark Mode", "Dark mode enabled (Ctrl+D to toggle)")
        else:
            self.setStyleSheet(self.get_light_stylesheet())
            QMessageBox.information(self, "Light Mode", "Light mode enabled (Ctrl+D to toggle)")
    
    def get_light_stylesheet(self) -> str:
        """Get light mode stylesheet with modern design."""
        return """
            QMainWindow, QDialog {
                background-color: #f5f7fa;
                color: #1a1a1a;
            }
            QWidget {
                background-color: #f5f7fa;
                color: #1a1a1a;
            }
            QLineEdit, QTextEdit, QPlainTextEdit {
                background-color: #ffffff;
                color: #1a1a1a;
                border: 2px solid #e0e6ed;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11px;
            }
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 2px solid #3498db;
                background-color: #ffffff;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3498db, stop:1 #2980b9);
                color: #ffffff;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5dade2, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2980b9, stop:1 #1f618d);
            }
            QListWidget, QListView {
                background-color: #ffffff;
                color: #1a1a1a;
                border: 2px solid #e0e6ed;
                border-radius: 6px;
                outline: none;
            }
            QListWidget::item {
                padding: 4px;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background-color: #ecf0f6;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5dade2, stop:1 #3498db);
                color: #ffffff;
            }
            QTabWidget {
                background-color: #f5f7fa;
                color: #1a1a1a;
                border: none;
            }
            QTabWidget::pane {
                border: 2px solid #e0e6ed;
                border-radius: 6px;
            }
            QTabBar::tab {
                background-color: #ecf0f6;
                color: #1a1a1a;
                padding: 10px 24px;
                border: none;
                margin-right: 2px;
                border-radius: 6px 6px 0 0;
                font-weight: 500;
            }
            QTabBar::tab:hover {
                background-color: #d4dce6;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3498db, stop:1 #2980b9);
                color: #ffffff;
            }
            QLabel {
                color: #1a1a1a;
                background-color: transparent;
            }
            QFrame {
                background-color: #ffffff;
                color: #1a1a1a;
                border: 2px solid #e0e6ed;
                border-radius: 6px;
            }
            QMenu {
                background-color: #ffffff;
                color: #1a1a1a;
                border: 2px solid #e0e6ed;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5dade2, stop:1 #3498db);
                color: #ffffff;
                border-radius: 4px;
            }
            QScrollBar:vertical {
                background-color: #f0f3f7;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #bdc3d0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a8aeb7;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QHeaderView::section {
                background-color: #ecf0f6;
                color: #1a1a1a;
                padding: 6px;
                border: none;
                border-bottom: 2px solid #e0e6ed;
            }
        """
    
    def get_dark_stylesheet(self) -> str:
        """Get dark mode stylesheet with modern design."""
        return """
            QMainWindow, QDialog {
                background-color: #1a1a2e;
                color: #e8e8e8;
            }
            QWidget {
                background-color: #1a1a2e;
                color: #e8e8e8;
            }
            QLineEdit, QTextEdit, QPlainTextEdit {
                background-color: #16213e;
                color: #e8e8e8;
                border: 2px solid #0f3460;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11px;
            }
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 2px solid #00d4ff;
                background-color: #16213e;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #00a8e8, stop:1 #0084c4);
                color: #ffffff;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #00d4ff, stop:1 #00a8e8);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #0084c4, stop:1 #006a9b);
            }
            QListWidget, QListView {
                background-color: #16213e;
                color: #e8e8e8;
                border: 2px solid #0f3460;
                border-radius: 6px;
                outline: none;
            }
            QListWidget::item {
                padding: 4px;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background-color: #0f3460;
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #00d4ff, stop:1 #00a8e8);
                color: #1a1a2e;
            }
            QTabWidget {
                background-color: #1a1a2e;
                color: #e8e8e8;
                border: none;
            }
            QTabWidget::pane {
                border: 2px solid #0f3460;
                border-radius: 6px;
            }
            QTabBar::tab {
                background-color: #0f3460;
                color: #e8e8e8;
                padding: 10px 24px;
                border: none;
                margin-right: 2px;
                border-radius: 6px 6px 0 0;
                font-weight: 500;
            }
            QTabBar::tab:hover {
                background-color: #16213e;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #00a8e8, stop:1 #0084c4);
                color: #1a1a2e;
            }
            QLabel {
                color: #e8e8e8;
                background-color: transparent;
            }
            QFrame {
                background-color: #16213e;
                color: #e8e8e8;
                border: 2px solid #0f3460;
                border-radius: 6px;
            }
            QMenu {
                background-color: #16213e;
                color: #e8e8e8;
                border: 2px solid #0f3460;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #00d4ff, stop:1 #00a8e8);
                color: #1a1a2e;
                border-radius: 4px;
            }
            QScrollBar:vertical {
                background-color: #0f3460;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #00a8e8;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00d4ff;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QHeaderView::section {
                background-color: #0f3460;
                color: #e8e8e8;
                padding: 6px;
                border: none;
                border-bottom: 2px solid #00a8e8;
            }
        """

    def init_ui(self):
        """Initialize the user interface."""
        # Apply light mode stylesheet by default
        self.setStyleSheet(self.get_light_stylesheet())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left side - File browser and image preview
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        open_button = QPushButton('📁 Open Image')
        open_button.clicked.connect(self.open_image)
        open_button.setMinimumHeight(35)
        open_button.setFont(QFont('System', 10))
        
        browse_button = QPushButton('📂 Browse Folder')
        browse_button.clicked.connect(self.browse_folder)
        browse_button.setMinimumHeight(35)
        browse_button.setFont(QFont('System', 10))
        
        edit_button = QPushButton('✏️ Edit Metadata')
        edit_button.clicked.connect(self.edit_metadata)
        edit_button.setMinimumHeight(35)
        edit_button.setFont(QFont('System', 10))
        
        export_button = QPushButton('💾 Export/Save')
        export_button.clicked.connect(self.export_image)
        export_button.setMinimumHeight(35)
        export_button.setFont(QFont('System', 10))
        
        button_layout.addWidget(open_button)
        button_layout.addWidget(browse_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(export_button)
        
        # Advanced menu button
        advanced_menu = QPushButton('⚙️ Advanced')
        advanced_menu.setMinimumHeight(35)
        advanced_menu.setFont(QFont('System', 10))
        
        # Create menu
        menu = QMenu(self)
        menu.addAction('🗺️ GPS Info', self.show_gps_info)
        menu.addAction('🔐 Privacy Report', self.show_privacy_report)
        menu.addAction('🛡️ Privacy Mode', self.enable_privacy_mode)
        menu.addAction('📷 Image Operations', self.show_image_operations)
        menu.addSeparator()
        menu.addAction('🌓 Dark Mode (Ctrl+D)', self.toggle_dark_mode)
        
        advanced_menu.setMenu(menu)
        button_layout.addWidget(advanced_menu)
        
        left_layout.addLayout(button_layout)
        
        # File list
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_selected)
        left_layout.addWidget(QLabel('Images in Folder:'))
        left_layout.addWidget(self.file_list)
        
        # Image preview area
        left_layout.addWidget(QLabel('Preview:'))
        preview_frame = QFrame()
        preview_frame.setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(5, 5, 5, 5)
        
        self.preview_label = QLabel('No image selected')
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(250)
        self.preview_label.setStyleSheet("color: #666; font-size: 14px;")
        preview_layout.addWidget(self.preview_label)
        
        left_layout.addWidget(preview_frame)
        
        # Right side - Metadata display
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        right_layout.addWidget(QLabel('Metadata Information:'))
        
        # Create tabs for different metadata sections
        self.tabs = QTabWidget()
        
        # Basic Info Tab
        self.basic_tab = QListWidget()
        self.tabs.addTab(self.basic_tab, '📄 Basic Info')
        
        # EXIF Data Tab
        self.exif_tab = QListWidget()
        self.tabs.addTab(self.exif_tab, '📷 EXIF Data')
        
        # Properties Tab
        self.properties_tab = QListWidget()
        self.tabs.addTab(self.properties_tab, '⚙️ Properties')
        
        right_layout.addWidget(self.tabs)
        
        # Splitter for resizable left and right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([700, 700])
        
        main_layout.addWidget(splitter)

    def open_image(self):
        """Open a single image file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Open Image',
            str(self.current_directory),
            'Image Files (*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp);;All Files (*)'
        )
        
        if file_path:
            self.current_file = Path(file_path)
            self.current_directory = self.current_file.parent
            self.load_image(self.current_file)

    def browse_folder(self):
        """Browse and load images from a folder."""
        folder = QFileDialog.getExistingDirectory(
            self,
            'Select Folder',
            str(self.current_directory)
        )
        
        if folder:
            self.current_directory = Path(folder)
            self.load_folder(self.current_directory)

    def load_folder(self, directory: Path):
        """Load all images from a folder."""
        self.image_list = MetadataParser.find_images_in_directory(directory)
        self.file_list.clear()
        
        for idx, image_path in enumerate(self.image_list):
            item = QListWidgetItem(image_path.name)
            item.setData(Qt.ItemDataRole.UserRole, idx)
            self.file_list.addItem(item)
        
        if self.image_list:
            self.file_list.setCurrentRow(0)
            self.load_image(self.image_list[0])

    def on_file_selected(self, item):
        """Handle file selection from the list."""
        idx = item.data(Qt.ItemDataRole.UserRole)
        if idx is not None and idx < len(self.image_list):
            self.load_image(self.image_list[idx])

    def load_image(self, file_path: Path):
        """Load and display image with metadata."""
        self.current_file = file_path
        
        # Update preview
        pixmap = QPixmap(str(file_path))
        if not pixmap.isNull():
            scaled = pixmap.scaledToHeight(250, Qt.TransformationMode.SmoothTransformation)
            self.preview_label.setPixmap(scaled)
        else:
            self.preview_label.setText('Cannot load image preview')
        
        # Load and display metadata
        metadata = MetadataParser.get_all_metadata(file_path)
        self.display_metadata(metadata)

    def display_metadata(self, metadata: dict):
        """Display metadata in the tabs."""
        # Clear previous data
        self.basic_tab.clear()
        self.exif_tab.clear()
        self.properties_tab.clear()
        
        # Display Basic Information
        basic_info = metadata.get('Basic Information', {})
        for key, value in basic_info.items():
            self.add_metadata_item(self.basic_tab, key, value)
        
        # Display EXIF Data
        exif_data = metadata.get('EXIF Data', {})
        if exif_data:
            for key, value in sorted(exif_data.items()):
                self.add_metadata_item(self.exif_tab, key, value)
        else:
            self.exif_tab.addItem('No EXIF data found')
        
        # Display Image Properties
        properties = metadata.get('Image Properties', {})
        for key, value in properties.items():
            self.add_metadata_item(self.properties_tab, key, value)

    @staticmethod
    def add_metadata_item(list_widget: QListWidget, key: str, value):
        """Add a metadata item to the list widget."""
        text = f"{key}: {value}"
        item = QListWidgetItem(text)
        item.setFont(QFont('Menlo', 10))
        list_widget.addItem(item)

    def edit_metadata(self):
        """Open dialog to edit metadata."""
        if not self.current_file:
            QMessageBox.warning(self, 'Warning', 'Please select an image first')
            return
        
        # Get current metadata
        metadata = MetadataParser.get_all_metadata(self.current_file)
        
        # Open edit dialog with file path
        dialog = EditMetadataDialog(self, metadata, self.current_file)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            edited_data = dialog.get_edited_data()
            file_timestamp = dialog.get_file_timestamp()
            
            # Create backup before editing
            backup_path = MetadataEditor.create_backup(self.current_file)
            if not backup_path:
                QMessageBox.critical(self, 'Error', 'Failed to create backup')
                return
            
            # Try to save edited metadata
            success = True
            if edited_data:
                if not MetadataEditor.edit_exif_data(self.current_file, edited_data):
                    success = False
            
            # Try to change file timestamp if provided
            if success and file_timestamp and file_timestamp.strip():
                if not MetadataEditor.set_file_timestamp(self.current_file, file_timestamp):
                    QMessageBox.warning(self, 'Warning', 'Metadata saved but failed to change file timestamp')
                    success = False
            
            if success:
                msg = f'✅ Metadata & properties updated successfully!\nBackup saved as: {backup_path.name}'
                if file_timestamp and file_timestamp.strip():
                    msg += f'\nFile timestamp changed to: {file_timestamp}'
                QMessageBox.information(self, 'Success', msg)
                # Reload image to show updated metadata
                self.load_image(self.current_file)
            else:
                QMessageBox.critical(self, 'Error', 'Failed to save metadata')
                # Restore from backup
                MetadataEditor.restore_backup(self.current_file, backup_path)

    def export_image(self):
        """Export or save the image with options."""
        if not self.current_file:
            QMessageBox.warning(self, 'Warning', 'Please select an image first')
            return
        
        # Create export options dialog
        export_dialog = QDialog(self)
        export_dialog.setWindowTitle('Export Options')
        export_dialog.setGeometry(300, 300, 400, 200)
        
        layout = QVBoxLayout(export_dialog)
        
        # Options
        layout.addWidget(QLabel('Choose export option:'))
        
        button_layout = QVBoxLayout()
        
        # Button 1: Export image copy
        copy_button = QPushButton('📸 Copy Image to Location')
        copy_button.clicked.connect(lambda: self.export_image_copy(export_dialog))
        button_layout.addWidget(copy_button)
        
        # Button 2: Export metadata to file
        metadata_button = QPushButton('📄 Export Metadata to Text')
        metadata_button.clicked.connect(lambda: self.export_metadata_text(export_dialog))
        button_layout.addWidget(metadata_button)
        
        # Button 3: Remove EXIF and export
        remove_exif_button = QPushButton('🔒 Export Without Metadata')
        remove_exif_button.clicked.connect(lambda: self.export_without_exif(export_dialog))
        button_layout.addWidget(remove_exif_button)
        
        # Button 4: Cancel
        cancel_button = QPushButton('❌ Cancel')
        cancel_button.clicked.connect(export_dialog.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        export_dialog.exec()

    def export_image_copy(self, parent_dialog):
        """Export a copy of the image."""
        export_path, _ = QFileDialog.getSaveFileName(
            self,
            'Export Image',
            str(self.current_directory / f"exported_{self.current_file.name}"),
            'Image Files (*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp);;All Files (*)'
        )
        
        if export_path:
            if MetadataEditor.export_image_copy(self.current_file, Path(export_path)):
                QMessageBox.information(self, 'Success', f'Image exported successfully!\n{export_path}')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to export image')
            parent_dialog.close()

    def export_metadata_text(self, parent_dialog):
        """Export metadata to a text file."""
        export_path, _ = QFileDialog.getSaveFileName(
            self,
            'Export Metadata',
            str(self.current_directory / f"{self.current_file.stem}_metadata.txt"),
            'Text Files (*.txt);;All Files (*)'
        )
        
        if export_path:
            metadata = MetadataParser.get_all_metadata(self.current_file)
            if MetadataEditor.export_metadata_to_file(self.current_file, metadata, Path(export_path)):
                QMessageBox.information(self, 'Success', f'Metadata exported successfully!\n{export_path}')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to export metadata')
            parent_dialog.close()

    def export_without_exif(self, parent_dialog):
        """Export image without EXIF data."""
        export_path, _ = QFileDialog.getSaveFileName(
            self,
            'Export Image Without Metadata',
            str(self.current_directory / f"no_exif_{self.current_file.name}"),
            'Image Files (*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp);;All Files (*)'
        )
        
        if export_path:
            if MetadataEditor.remove_exif_data(self.current_file, Path(export_path)):
                QMessageBox.information(
                    self, 
                    'Success', 
                    f'Image exported without metadata!\n{export_path}'
                )
            else:
                QMessageBox.critical(self, 'Error', 'Failed to remove metadata')
            parent_dialog.close()

    def show_gps_info(self):
        """Show GPS information for current image."""
        if not self.current_file:
            QMessageBox.warning(self, 'Warning', 'Please select an image first')
            return
        
        gps_info = GPSHandler.get_gps_info(self.current_file)
        
        message = "📍 GPS Information:\n\n"
        if gps_info['has_gps']:
            lat, lon = gps_info['coordinates']
            message += f"Latitude: {lat:.6f}°\n"
            message += f"Longitude: {lon:.6f}°\n"
            message += f"Location: {gps_info['location_name']}\n"
            if gps_info['altitude']:
                message += f"Altitude: {gps_info['altitude']:.2f}m"
        else:
            message += "No GPS data found in this image"
        
        QMessageBox.information(self, 'GPS Information', message)
    
    def show_privacy_report(self):
        """Show privacy report for current image."""
        if not self.current_file:
            QMessageBox.warning(self, 'Warning', 'Please select an image first')
            return
        
        report = PrivacyHandler.get_privacy_report(self.current_file)
        
        message = f"🔐 Privacy Report for {report['file']}:\n\n"
        message += f"Risk Level: {report['risk_level']}\n\n"
        message += f"Has GPS Data: {'Yes' if report['has_gps'] else 'No'}\n"
        message += f"Has Timestamps: {'Yes' if report['has_timestamp'] else 'No'}\n"
        message += f"Has Camera Info: {'Yes' if report['has_camera_info'] else 'No'}\n"
        message += f"Has Personal Info: {'Yes' if report['has_personal_info'] else 'No'}\n"
        message += f"\nSensitive Fields Found: {report['sensitive_fields_found']}"
        
        QMessageBox.information(self, 'Privacy Report', message)
    
    def enable_privacy_mode(self):
        """Enable privacy mode to remove sensitive data."""
        if not self.current_file:
            QMessageBox.warning(self, 'Warning', 'Please select an image first')
            return
        
        # Create backup
        backup_path = MetadataEditor.create_backup(self.current_file)
        if not backup_path:
            QMessageBox.critical(self, 'Error', 'Failed to create backup')
            return
        
        if PrivacyHandler.privacy_mode(self.current_file):
            QMessageBox.information(
                self,
                'Success',
                'Privacy mode enabled! Sensitive data removed.\nBackup saved as: ' + backup_path.name
            )
            self.load_image(self.current_file)
        else:
            QMessageBox.critical(self, 'Error', 'Failed to enable privacy mode')
            PrivacyHandler.remove_gps_data(self.current_file)
    
    def show_image_operations(self):
        """Show image operations dialog."""
        if not self.current_file:
            QMessageBox.warning(self, 'Warning', 'Please select an image first')
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle('📷 Image Operations')
        dialog.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Resize button
        resize_button = QPushButton('🔍 Resize Image')
        resize_button.clicked.connect(lambda: self.resize_image_dialog())
        layout.addWidget(resize_button)
        
        # Compress button
        compress_button = QPushButton('🗜️ Compress Image')
        compress_button.clicked.connect(lambda: self.compress_image_dialog())
        layout.addWidget(compress_button)
        
        # Convert format button
        convert_button = QPushButton('🔄 Convert Format')
        convert_button.clicked.connect(lambda: self.convert_format_dialog())
        layout.addWidget(convert_button)
        
        # Show image info
        info_button = QPushButton('ℹ️ Image Information')
        info_button.clicked.connect(lambda: self.show_image_info())
        layout.addWidget(info_button)
        
        # Close button
        close_button = QPushButton('Close')
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        
        dialog.exec()
    
    def resize_image_dialog(self):
        """Show resize image dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle('Resize Image')
        dialog.setGeometry(400, 400, 300, 200)
        
        layout = QFormLayout(dialog)
        
        width_input = QSpinBox()
        width_input.setRange(1, 10000)
        width_input.setValue(800)
        layout.addRow('Width (px):', width_input)
        
        height_input = QSpinBox()
        height_input.setRange(1, 10000)
        height_input.setValue(600)
        layout.addRow('Height (px):', height_input)
        
        maintain_aspect = QCheckBox('Maintain Aspect Ratio')
        maintain_aspect.setChecked(True)
        layout.addRow(maintain_aspect)
        
        button_layout = QHBoxLayout()
        resize_button = QPushButton('Resize')
        cancel_button = QPushButton('Cancel')
        
        def do_resize():
            output_path = self.current_file.parent / f"resized_{self.current_file.name}"
            if ImageOperations.resize_image(self.current_file, width_input.value(), 
                                           height_input.value(), maintain_aspect.isChecked(), output_path):
                QMessageBox.information(self, 'Success', f'Image resized!\nSaved as: resized_{self.current_file.name}')
                dialog.close()
            else:
                QMessageBox.critical(self, 'Error', 'Failed to resize image')
        
        resize_button.clicked.connect(do_resize)
        cancel_button.clicked.connect(dialog.close)
        
        button_layout.addWidget(resize_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)
        
        dialog.exec()
    
    def compress_image_dialog(self):
        """Show compress image dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle('Compress Image')
        dialog.setGeometry(400, 400, 300, 150)
        
        layout = QFormLayout(dialog)
        
        quality_input = QSpinBox()
        quality_input.setRange(1, 100)
        quality_input.setValue(85)
        layout.addRow('Quality (1-100):', quality_input)
        
        button_layout = QHBoxLayout()
        compress_button = QPushButton('Compress')
        cancel_button = QPushButton('Cancel')
        
        def do_compress():
            output_path = self.current_file.parent / f"compressed_{self.current_file.name}"
            if ImageOperations.compress_image(self.current_file, quality_input.value(), output_path):
                QMessageBox.information(self, 'Success', f'Image compressed!\nSaved as: compressed_{self.current_file.name}')
                dialog.close()
            else:
                QMessageBox.critical(self, 'Error', 'Failed to compress image')
        
        compress_button.clicked.connect(do_compress)
        cancel_button.clicked.connect(dialog.close)
        
        button_layout.addWidget(compress_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)
        
        dialog.exec()
    
    def convert_format_dialog(self):
        """Show format conversion dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle('Convert Format')
        dialog.setGeometry(400, 400, 300, 150)
        
        layout = QFormLayout(dialog)
        
        format_combo = QComboBox()
        format_combo.addItems(['jpg', 'png', 'webp', 'bmp', 'gif'])
        layout.addRow('Target Format:', format_combo)
        
        button_layout = QHBoxLayout()
        convert_button = QPushButton('Convert')
        cancel_button = QPushButton('Cancel')
        
        def do_convert():
            output_path = self.current_file.parent / f"{self.current_file.stem}.{format_combo.currentText()}"
            if ImageOperations.convert_format(self.current_file, format_combo.currentText(), output_path):
                QMessageBox.information(self, 'Success', f'Image converted!\nSaved as: {output_path.name}')
                dialog.close()
            else:
                QMessageBox.critical(self, 'Error', 'Failed to convert image')
        
        convert_button.clicked.connect(do_convert)
        cancel_button.clicked.connect(dialog.close)
        
        button_layout.addWidget(convert_button)
        button_layout.addWidget(cancel_button)
        layout.addRow(button_layout)
        
        dialog.exec()
    
    def show_image_info(self):
        """Show comprehensive image information."""
        if not self.current_file:
            return
        
        info = ImageOperations.get_image_info(self.current_file)
        
        message = "📊 Image Information:\n\n"
        message += f"Format: {info.get('format', 'Unknown')}\n"
        message += f"Dimensions: {info.get('width', 0)}x{info.get('height', 0)} px\n"
        message += f"Size: {info.get('size_mb', 0):.2f} MB\n"
        message += f"Color Mode: {info.get('mode', 'Unknown')}\n"
        message += f"DPI: {info.get('dpi', (72, 72))}\n"
        if info.get('has_animation'):
            message += f"Animation Frames: {info.get('frame_count', 1)}"
        
        QMessageBox.information(self, 'Image Information', message)

    @staticmethod
    def create_icon():
        """Create a simple icon for the window."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        return QIcon(pixmap)


def main():
    """Main entry point."""
    app_instance = None
    try:
        app_instance = __import__('PyQt6.QtWidgets').QtWidgets.QApplication.instance()
        if app_instance is None:
            app_instance = __import__('PyQt6.QtWidgets').QtWidgets.QApplication(sys.argv)
    except:
        app_instance = __import__('PyQt6.QtWidgets').QtWidgets.QApplication(sys.argv)
    
    window = MetadataViewer()
    window.show()
    sys.exit(app_instance.exec())


if __name__ == '__main__':
    main()
