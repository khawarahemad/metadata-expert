"""
Privacy and security features for metadata management.
Supports metadata encryption, selective removal, and privacy mode.
"""

from pathlib import Path
from PIL import Image
import piexif
import json
from typing import List, Dict, Optional


class PrivacyHandler:
    """Handle privacy and security features."""
    
    # Fields to remove in privacy mode
    SENSITIVE_FIELDS = {
        'GPS': ['GPSInfo', 'GPSLatitude', 'GPSLongitude', 'GPSAltitude'],
        'DateTime': ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized'],
        'Camera': ['Make', 'Model', 'LensModel'],
        'Personal': ['Artist', 'Copyright', 'UserComment']
    }
    
    @staticmethod
    def strip_metadata(file_path: Path, preserve_fields: Optional[List[str]] = None) -> bool:
        """
        Remove all metadata from image.
        
        Args:
            file_path: Path to image
            preserve_fields: List of fields to keep
        """
        try:
            image = Image.open(file_path)
            
            # Create image data without EXIF
            data = list(image.getdata())
            image_no_exif = Image.new(image.mode, image.size)
            image_no_exif.putdata(data)
            
            # Save without EXIF
            image_no_exif.save(file_path)
            return True
        except Exception as e:
            print(f"Error stripping metadata: {e}")
            return False
    
    @staticmethod
    def privacy_mode(file_path: Path, categories: List[str] = None) -> bool:
        """
        Enable privacy mode: remove sensitive metadata categories.
        
        Categories: 'GPS', 'DateTime', 'Camera', 'Personal', 'All'
        """
        try:
            if categories is None:
                categories = ['GPS', 'DateTime', 'Personal']
            
            exif_dict = piexif.load(str(file_path))
            
            if 'All' in categories:
                # Remove all EXIF data
                return PrivacyHandler.strip_metadata(file_path)
            
            # Remove specific categories
            for category in categories:
                if category in PrivacyHandler.SENSITIVE_FIELDS:
                    fields_to_remove = PrivacyHandler.SENSITIVE_FIELDS[category]
                    
                    for ifd_name in ("0th", "Exif", "GPS", "1st"):
                        if ifd_name in exif_dict:
                            ifd = exif_dict[ifd_name]
                            for tag, value in list(ifd.items()):
                                try:
                                    tag_name = piexif.TAGS[ifd_name][tag]["name"]
                                    if tag_name in fields_to_remove:
                                        del ifd[tag]
                                except:
                                    pass
            
            # Save modified image
            exif_bytes = piexif.dump(exif_dict)
            image = Image.open(file_path)
            image.save(file_path, exif=exif_bytes)
            return True
        except Exception as e:
            print(f"Error enabling privacy mode: {e}")
            return False
    
    @staticmethod
    def get_sensitive_metadata(file_path: Path) -> Dict[str, List[str]]:
        """Get all sensitive metadata found in image."""
        sensitive_data = {}
        
        try:
            exif_dict = piexif.load(str(file_path))
            
            for ifd_name in ("0th", "Exif", "GPS", "1st"):
                ifd = exif_dict.get(ifd_name, {})
                
                for tag, value in ifd.items():
                    try:
                        tag_name = piexif.TAGS[ifd_name][tag]["name"]
                        
                        for category, fields in PrivacyHandler.SENSITIVE_FIELDS.items():
                            if tag_name in fields:
                                if category not in sensitive_data:
                                    sensitive_data[category] = []
                                sensitive_data[category].append(f"{tag_name}: {str(value)[:50]}")
                    except:
                        pass
        except Exception as e:
            print(f"Error scanning sensitive metadata: {e}")
        
        return sensitive_data
    
    @staticmethod
    def encrypt_metadata(metadata: Dict, password: str) -> str:
        """
        Simple metadata encryption (for storage).
        Note: For production, use proper encryption library like cryptography.
        """
        import base64
        
        try:
            json_str = json.dumps(metadata)
            # Simple encoding (NOT secure - use proper encryption in production)
            encoded = base64.b64encode(json_str.encode()).decode()
            return encoded
        except Exception as e:
            print(f"Error encrypting metadata: {e}")
            return ""
    
    @staticmethod
    def decrypt_metadata(encrypted_data: str, password: str) -> Dict:
        """
        Decrypt metadata.
        Note: For production, use proper encryption library.
        """
        import base64
        
        try:
            decoded = base64.b64decode(encrypted_data).decode()
            return json.loads(decoded)
        except Exception as e:
            print(f"Error decrypting metadata: {e}")
            return {}
    
    @staticmethod
    def get_privacy_report(file_path: Path) -> Dict:
        """Generate privacy report for an image."""
        sensitive = PrivacyHandler.get_sensitive_metadata(file_path)
        
        report = {
            'file': file_path.name,
            'has_gps': 'GPS' in sensitive,
            'has_timestamp': 'DateTime' in sensitive,
            'has_camera_info': 'Camera' in sensitive,
            'has_personal_info': 'Personal' in sensitive,
            'sensitive_fields_found': sum(len(v) for v in sensitive.values()),
            'details': sensitive,
            'risk_level': 'HIGH' if sensitive else 'LOW'
        }
        
        return report
    
    @staticmethod
    def batch_privacy_mode(directory: Path, categories: List[str] = None) -> Dict:
        """
        Apply privacy mode to all images in a directory.
        Returns: Statistics of processed images
        """
        stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        try:
            for image_file in directory.rglob('*'):
                if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tiff', '.gif']:
                    stats['total_processed'] += 1
                    
                    if PrivacyHandler.privacy_mode(image_file, categories):
                        stats['successful'] += 1
                    else:
                        stats['failed'] += 1
                        stats['errors'].append(str(image_file))
        except Exception as e:
            print(f"Error in batch processing: {e}")
        
        return stats
    
    @staticmethod
    def secure_delete(file_path: Path) -> bool:
        """
        Securely delete a file by overwriting it multiple times.
        """
        try:
            import os
            
            # Overwrite file 3 times
            file_size = file_path.stat().st_size
            
            for _ in range(3):
                with open(file_path, 'wb') as f:
                    f.write(b'\x00' * file_size)
            
            # Delete the file
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error securely deleting file: {e}")
            return False
