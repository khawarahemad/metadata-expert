"""
Metadata editing and export utilities.
Allows editing and saving metadata back to image files.
Supports comprehensive EXIF fields and file timestamp modification.
"""

from pathlib import Path
from PIL import Image
import piexif
from typing import Dict, Optional, Tuple
import shutil
from datetime import datetime
import os
import time


class MetadataEditor:
    """Edit and export image metadata with comprehensive field support."""

    # Comprehensive EXIF field mapping for all major metadata
    # Only includes fields that exist in piexif library
    EXIF_FIELD_MAPPING = {
        # Date & Time
        "DateTime": ("0th", piexif.ImageIFD.DateTime),
        "DateTimeOriginal": ("Exif", piexif.ExifIFD.DateTimeOriginal),
        "DateTimeDigitized": ("Exif", piexif.ExifIFD.DateTimeDigitized),
        
        # Creator & Copyright
        "Artist": ("0th", piexif.ImageIFD.Artist),
        "Copyright": ("0th", piexif.ImageIFD.Copyright),
        "ImageDescription": ("0th", piexif.ImageIFD.ImageDescription),
        "Software": ("0th", piexif.ImageIFD.Software),
        
        # Camera Equipment
        "Make": ("0th", piexif.ImageIFD.Make),
        "Model": ("0th", piexif.ImageIFD.Model),
        "LensModel": ("Exif", piexif.ExifIFD.LensModel),
        
        # Exposure Settings
        "ExposureTime": ("Exif", piexif.ExifIFD.ExposureTime),
        "FNumber": ("Exif", piexif.ExifIFD.FNumber),
        "ISOSpeedRatings": ("Exif", piexif.ExifIFD.ISOSpeedRatings),
        "ExposureBiasValue": ("Exif", piexif.ExifIFD.ExposureBiasValue),
        "MeteringMode": ("Exif", piexif.ExifIFD.MeteringMode),
        "Flash": ("Exif", piexif.ExifIFD.Flash),
        "WhiteBalance": ("Exif", piexif.ExifIFD.WhiteBalance),
        
        # Focal & Focus
        "FocalLength": ("Exif", piexif.ExifIFD.FocalLength),
        "FocalLengthIn35mmFilm": ("Exif", piexif.ExifIFD.FocalLengthIn35mmFilm),
        "SubjectDistance": ("Exif", piexif.ExifIFD.SubjectDistance),
        
        # Image Properties
        "Orientation": ("0th", piexif.ImageIFD.Orientation),
        "XResolution": ("0th", piexif.ImageIFD.XResolution),
        "YResolution": ("0th", piexif.ImageIFD.YResolution),
        "ResolutionUnit": ("0th", piexif.ImageIFD.ResolutionUnit),
        
        # Location/GPS
        "GPSVersionID": ("GPS", piexif.GPSIFD.GPSVersionID),
        "GPSLatitude": ("GPS", piexif.GPSIFD.GPSLatitude),
        "GPSLatitudeRef": ("GPS", piexif.GPSIFD.GPSLatitudeRef),
        "GPSLongitude": ("GPS", piexif.GPSIFD.GPSLongitude),
        "GPSLongitudeRef": ("GPS", piexif.GPSIFD.GPSLongitudeRef),
        "GPSAltitude": ("GPS", piexif.GPSIFD.GPSAltitude),
        "GPSAltitudeRef": ("GPS", piexif.GPSIFD.GPSAltitudeRef),
        "GPSTimeStamp": ("GPS", piexif.GPSIFD.GPSTimeStamp),
        "GPSDateStamp": ("GPS", piexif.GPSIFD.GPSDateStamp),
        
        # Additional Metadata
        "UserComment": ("Exif", piexif.ExifIFD.UserComment),
    }

    @staticmethod
    def edit_exif_data(file_path: Path, exif_updates: Dict) -> bool:
        """
        Edit EXIF data in an image file.
        
        Args:
            file_path: Path to the image file
            exif_updates: Dictionary of EXIF tags to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load existing EXIF data
            exif_dict = piexif.load(str(file_path))
            
            # Update EXIF data
            for key, value in exif_updates.items():
                if key not in MetadataEditor.EXIF_FIELD_MAPPING:
                    continue
                
                mapping = MetadataEditor.EXIF_FIELD_MAPPING[key]
                ifd_name, tag = mapping[0], mapping[1]
                
                if tag is None:
                    continue
                
                try:
                    # Convert string to appropriate format
                    if isinstance(value, str):
                        value = value.encode('utf-8')
                    
                    # Ensure IFD exists
                    if ifd_name not in exif_dict or exif_dict[ifd_name] is None:
                        exif_dict[ifd_name] = {}
                    
                    exif_dict[ifd_name][tag] = value
                except Exception as e:
                    print(f"Error setting {key}: {e}")
                    continue
            
            # Convert EXIF dict back to bytes
            exif_bytes = piexif.dump(exif_dict)
            
            # Save image with new EXIF data
            image = Image.open(file_path)
            image.save(file_path, exif=exif_bytes)
            
            return True
        except Exception as e:
            print(f"Error editing EXIF data: {e}")
            return False
    
    @staticmethod
    def set_file_timestamp(file_path: Path, datetime_str: str) -> bool:
        """
        Set the file's modification and access timestamps.
        Allows changing the file's apparent date to make edits untraceable.
        
        Args:
            file_path: Path to the file
            datetime_str: DateTime string in format 'YYYY-MM-DD HH:MM:SS'
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Parse datetime string
            dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            # Convert to timestamp
            timestamp = time.mktime(dt.timetuple())
            
            # Set both access and modification times
            os.utime(file_path, (timestamp, timestamp))
            return True
        except Exception as e:
            print(f"Error setting file timestamp: {e}")
            return False
    
    @staticmethod
    def get_file_timestamp(file_path: Path) -> str:
        """
        Get the file's modification timestamp.
        
        Args:
            file_path: Path to the file
            
        Returns:
            DateTime string in format 'YYYY-MM-DD HH:MM:SS'
        """
        try:
            mod_time = os.path.getmtime(file_path)
            dt = datetime.fromtimestamp(mod_time)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error getting file timestamp: {e}")
            return ""

    @staticmethod
    def create_backup(file_path: Path) -> Optional[Path]:
        """
        Create a backup of the original file.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            Path to backup file, or None if failed
        """
        try:
            backup_path = file_path.parent / f"{file_path.stem}_backup{file_path.suffix}"
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None

    @staticmethod
    def restore_backup(original_path: Path, backup_path: Path) -> bool:
        """
        Restore a file from backup.
        
        Args:
            original_path: Path to the original file
            backup_path: Path to the backup file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.copy2(backup_path, original_path)
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False

    @staticmethod
    def export_metadata_to_file(file_path: Path, metadata: Dict, export_path: Path) -> bool:
        """
        Export metadata to a text or JSON file.
        
        Args:
            file_path: Path to the original image file
            metadata: Dictionary containing all metadata
            export_path: Path where to save the metadata file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(f"Metadata Export for: {file_path.name}\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                for section, data in metadata.items():
                    f.write(f"\n[{section}]\n")
                    f.write("-" * 80 + "\n")
                    if isinstance(data, dict):
                        for key, value in data.items():
                            f.write(f"{key}: {value}\n")
                    else:
                        f.write(f"{data}\n")
                
            return True
        except Exception as e:
            print(f"Error exporting metadata: {e}")
            return False

    @staticmethod
    def export_image_copy(file_path: Path, export_path: Path) -> bool:
        """
        Export a copy of the image to a specified location.
        
        Args:
            file_path: Path to the original image
            export_path: Path where to save the copy
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.copy2(file_path, export_path)
            return True
        except Exception as e:
            print(f"Error exporting image: {e}")
            return False

    @staticmethod
    def remove_exif_data(file_path: Path, export_path: Path) -> bool:
        """
        Create a copy of image with all EXIF data removed.
        
        Args:
            file_path: Path to the original image
            export_path: Path where to save the stripped image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            image = Image.open(file_path)
            
            # Create a copy without EXIF data
            data = list(image.getdata())
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(data)
            
            # Copy basic properties
            if hasattr(image, 'info'):
                for key in ('duration', 'loop'):
                    if key in image.info:
                        image_without_exif.info[key] = image.info[key]
            
            image_without_exif.save(export_path)
            return True
        except Exception as e:
            print(f"Error removing EXIF data: {e}")
            return False
