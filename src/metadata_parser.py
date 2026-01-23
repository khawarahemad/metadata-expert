"""
Metadata parsing utilities for image files.
Extracts EXIF data, file information, and image properties.
"""

from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import piexif
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class MetadataParser:
    """Parse and extract metadata from image files."""

    # Supported image formats
    SUPPORTED_FORMATS = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
        '.webp', '.ico', '.ppm', '.pgm', '.pbm', '.pnm'
    }

    @staticmethod
    def is_supported_image(file_path: Path) -> bool:
        """Check if file is a supported image format."""
        return file_path.suffix.lower() in MetadataParser.SUPPORTED_FORMATS

    @staticmethod
    def get_basic_info(file_path: Path) -> Dict:
        """Extract basic file and image information."""
        try:
            file_stat = file_path.stat()
            image = Image.open(file_path)
            
            basic_info = {
                'Filename': file_path.name,
                'File Path': str(file_path),
                'File Size': MetadataParser._format_bytes(file_stat.st_size),
                'File Format': image.format,
                'Image Width': f"{image.width} px",
                'Image Height': f"{image.height} px",
                'Image Mode': image.mode,
                'DPI': str(image.info.get('dpi', 'Not specified')),
            }
            
            # Add modification date
            mod_time = datetime.fromtimestamp(file_stat.st_mtime)
            basic_info['Modified Date'] = mod_time.strftime('%Y-%m-%d %H:%M:%S')
            
            return basic_info
        except Exception as e:
            return {'Error': str(e)}

    @staticmethod
    def get_exif_data(file_path: Path) -> Dict:
        """Extract EXIF data from image."""
        exif_data = {}
        
        try:
            # Try using piexif for comprehensive EXIF data
            exif_dict = piexif.load(str(file_path))
            
            # Process different EXIF categories
            for ifd_name in ("0th", "Exif", "GPS", "1st"):
                ifd = exif_dict.get(ifd_name, {})
                if not ifd:
                    continue
                    
                for tag, value in ifd.items():
                    try:
                        tag_name = piexif.TAGS[ifd_name][tag]["name"]
                    except:
                        tag_name = str(tag)
                    
                    try:
                        if isinstance(value, bytes):
                            value = value.decode('utf-8', errors='ignore').strip()
                        else:
                            value = str(value).strip()
                        
                        # Only add non-empty values
                        if value and value != '':
                            exif_data[tag_name] = value
                    except:
                        try:
                            value = str(value)[:100].strip()
                            if value and value != '':
                                exif_data[tag_name] = value
                        except:
                            pass
        
        except Exception as e:
            # Fallback to PIL's EXIF extraction
            try:
                image = Image.open(file_path)
                exif = image.getexif()
                
                if exif:
                    for tag_id, value in exif.items():
                        try:
                            tag_name = TAGS.get(tag_id, str(tag_id))
                        except:
                            tag_name = str(tag_id)
                        
                        try:
                            if isinstance(value, bytes):
                                value = value.decode('utf-8', errors='ignore').strip()
                            else:
                                value = str(value).strip()
                            
                            # Only add non-empty values
                            if value and value != '':
                                exif_data[tag_name] = value
                        except:
                            try:
                                value = str(value)[:100].strip()
                                if value and value != '':
                                    exif_data[tag_name] = value
                            except:
                                pass
            except Exception:
                pass
        
        return exif_data if exif_data else {'Note': 'No EXIF data found'}

    @staticmethod
    def get_image_properties(file_path: Path) -> Dict:
        """Extract additional image properties."""
        properties = {}
        
        try:
            image = Image.open(file_path)
            
            # Color profile info
            if 'icc_profile' in image.info:
                properties['Has Color Profile'] = 'Yes'
            else:
                properties['Has Color Profile'] = 'No'
            
            # Animation info
            if hasattr(image, 'is_animated'):
                properties['Is Animated'] = 'Yes' if image.is_animated else 'No'
                if image.is_animated:
                    properties['Number of Frames'] = str(getattr(image, 'n_frames', 'Unknown'))
            
            # Check for transparency
            if image.mode in ('RGBA', 'LA', 'PA') or 'transparency' in image.info:
                properties['Has Transparency'] = 'Yes'
            else:
                properties['Has Transparency'] = 'No'
            
            # Image info
            for key, value in image.info.items():
                if key not in ('icc_profile', 'transparency', 'dpi'):
                    try:
                        properties[key] = str(value)[:100]
                    except:
                        pass
        
        except Exception as e:
            properties['Error'] = str(e)
        
        return properties

    @staticmethod
    def get_all_metadata(file_path: Path) -> Dict:
        """Get all metadata for an image file."""
        if not MetadataParser.is_supported_image(file_path):
            return {'Error': 'Unsupported file format'}
        
        return {
            'Basic Information': MetadataParser.get_basic_info(file_path),
            'EXIF Data': MetadataParser.get_exif_data(file_path),
            'Image Properties': MetadataParser.get_image_properties(file_path),
        }

    @staticmethod
    def _format_bytes(bytes_size: int) -> str:
        """Format bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"

    @staticmethod
    def find_images_in_directory(directory: Path) -> List[Path]:
        """Find all supported image files in a directory."""
        images = []
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file() and MetadataParser.is_supported_image(file_path):
                    images.append(file_path)
        except Exception:
            pass
        return sorted(images)
