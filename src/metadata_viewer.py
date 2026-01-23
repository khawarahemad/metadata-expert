"""
Main GUI application for Metadata Viewer.
Modern PyQt6-based interface for viewing image metadata.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QPushButton, QFileDialog, QLabel, QScrollArea, QFrame,
    QListWidget, QListWidgetItem, QTabWidget, QDialog, QLineEdit,
    QFormLayout, QMessageBox, QDialogButtonBox
)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QSize, QTimer
from metadata_parser import MetadataParser
from metadata_editor import MetadataEditor


class EditMetadataDialog(QDialog):
    """Dialog for editing metadata fields."""
    
    def __init__(self, parent=None, metadata=None):
        super().__init__(parent)
        self.metadata = metadata or {}
        self.edited_data = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize the dialog UI."""
        self.setWindowTitle('Edit Image Metadata')
        self.setGeometry(50, 50, 950, 900)
        
        main_layout = QVBoxLayout(self)
        
        # Info label
        info_label = QLabel('ℹ️ Original value shown in gray, edit in the input field - Shows ALL available metadata from image')
        info_font = QFont('System', 10)
        info_font.setItalic(True)
        info_label.setFont(info_font)
        info_label.setStyleSheet("color: #666;")
        main_layout.addWidget(info_label)
        
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
            '📅 Date & Time': ['date', 'time', 'datetime', 'timestamp'],
            '👤 Creator Info': ['artist', 'author', 'copyright', 'software', 'description'],
            '📷 Camera Info': ['make', 'model', 'lens', 'equipment', 'camera'],
            '🎯 Exposure Settings': ['exposure', 'iso', 'shutter', 'aperture', 'f-number', 'metering', 'program'],
            '🔍 Focus & Flash': ['focal', 'flash', 'focus', 'distance'],
            '🎨 Image Properties': ['orientation', 'resolution', 'dpi', 'color', 'saturation', 'contrast', 'brightness', 'white', 'balance'],
            '🌍 Location': ['gps', 'latitude', 'longitude', 'altitude', 'location'],
            '📝 Additional Info': ['subject', 'keywords', 'comment', 'unique'],
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
        self.accept()
    
    def get_edited_data(self):
        """Return the edited metadata."""
        return self.edited_data


class MetadataViewer(QMainWindow):
    """Main application window for viewing image metadata."""

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.current_directory = Path.home()
        self.image_list = []
        self.current_index = 0
        
        self.init_ui()
        self.setWindowTitle('Metadata Viewer')
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowIcon(self.create_icon())

    def init_ui(self):
        """Initialize the user interface."""
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
        open_button.setFont(QFont('System', 11))
        
        browse_button = QPushButton('📂 Browse Folder')
        browse_button.clicked.connect(self.browse_folder)
        browse_button.setMinimumHeight(35)
        browse_button.setFont(QFont('System', 11))
        
        edit_button = QPushButton('✏️ Edit Metadata')
        edit_button.clicked.connect(self.edit_metadata)
        edit_button.setMinimumHeight(35)
        edit_button.setFont(QFont('System', 11))
        
        export_button = QPushButton('💾 Export/Save')
        export_button.clicked.connect(self.export_image)
        export_button.setMinimumHeight(35)
        export_button.setFont(QFont('System', 11))
        
        button_layout.addWidget(open_button)
        button_layout.addWidget(browse_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(export_button)
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
        
        # Open edit dialog
        dialog = EditMetadataDialog(self, metadata)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            edited_data = dialog.get_edited_data()
            
            # Create backup before editing
            backup_path = MetadataEditor.create_backup(self.current_file)
            if not backup_path:
                QMessageBox.critical(self, 'Error', 'Failed to create backup')
                return
            
            # Try to save edited metadata
            if MetadataEditor.edit_exif_data(self.current_file, edited_data):
                QMessageBox.information(
                    self, 
                    'Success', 
                    f'Metadata saved successfully!\nBackup saved as: {backup_path.name}'
                )
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
