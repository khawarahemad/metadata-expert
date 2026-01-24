"""
Advanced image operations for batch processing.
Supports resize, compress, format conversion, and more.
"""

from pathlib import Path
from PIL import Image
from typing import Dict, List, Tuple, Optional


class ImageOperations:
    """Advanced image processing operations."""
    
    SUPPORTED_FORMATS = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.gif': 'GIF',
        '.bmp': 'BMP',
        '.tiff': 'TIFF',
        '.webp': 'WEBP',
        '.ico': 'ICO'
    }
    
    @staticmethod
    def resize_image(file_path: Path, width: int, height: int, 
                    maintain_aspect: bool = True, output_path: Optional[Path] = None) -> bool:
        """
        Resize image to specified dimensions.
        
        Args:
            file_path: Input image path
            width: Target width in pixels
            height: Target height in pixels
            maintain_aspect: Keep aspect ratio
            output_path: Output file path (defaults to input)
        """
        try:
            image = Image.open(file_path)
            
            if maintain_aspect:
                image.thumbnail((width, height), Image.Resampling.LANCZOS)
            else:
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            
            save_path = output_path or file_path
            image.save(save_path, quality=95)
            return True
        except Exception as e:
            print(f"Error resizing image: {e}")
            return False
    
    @staticmethod
    def compress_image(file_path: Path, quality: int = 85, 
                      output_path: Optional[Path] = None) -> bool:
        """
        Compress image to reduce file size.
        
        Args:
            file_path: Input image path
            quality: Compression quality (1-100)
            output_path: Output file path
        """
        try:
            image = Image.open(file_path)
            
            save_path = output_path or file_path
            image.save(save_path, quality=quality, optimize=True)
            return True
        except Exception as e:
            print(f"Error compressing image: {e}")
            return False
    
    @staticmethod
    def convert_format(file_path: Path, target_format: str, 
                      output_path: Optional[Path] = None) -> bool:
        """
        Convert image to different format.
        
        Args:
            file_path: Input image path
            target_format: Target format (jpg, png, webp, etc.)
            output_path: Output file path
        """
        try:
            image = Image.open(file_path)
            
            # Convert RGBA to RGB for JPEG
            if target_format.lower() == 'jpg' and image.mode == 'RGBA':
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                image = rgb_image
            
            if output_path is None:
                output_path = file_path.parent / f"{file_path.stem}.{target_format}"
            
            image.save(output_path)
            return True
        except Exception as e:
            print(f"Error converting format: {e}")
            return False
    
    @staticmethod
    def batch_resize(directory: Path, width: int, height: int, 
                    output_dir: Optional[Path] = None) -> Dict:
        """
        Resize all images in a directory.
        """
        stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'total_original_size': 0,
            'total_new_size': 0
        }
        
        try:
            output_dir = output_dir or directory / 'resized'
            output_dir.mkdir(exist_ok=True)
            
            for image_file in directory.glob('*'):
                if image_file.suffix.lower() in ImageOperations.SUPPORTED_FORMATS:
                    stats['total'] += 1
                    original_size = image_file.stat().st_size
                    
                    output_path = output_dir / image_file.name
                    
                    if ImageOperations.resize_image(image_file, width, height, True, output_path):
                        stats['successful'] += 1
                        stats['total_original_size'] += original_size
                        stats['total_new_size'] += output_path.stat().st_size
                    else:
                        stats['failed'] += 1
        except Exception as e:
            print(f"Error in batch resize: {e}")
        
        return stats
    
    @staticmethod
    def batch_compress(directory: Path, quality: int = 85, 
                      output_dir: Optional[Path] = None) -> Dict:
        """
        Compress all images in a directory.
        """
        stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'total_original_size': 0,
            'total_new_size': 0,
            'compression_ratio': 0.0
        }
        
        try:
            output_dir = output_dir or directory / 'compressed'
            output_dir.mkdir(exist_ok=True)
            
            for image_file in directory.glob('*'):
                if image_file.suffix.lower() in ImageOperations.SUPPORTED_FORMATS:
                    stats['total'] += 1
                    original_size = image_file.stat().st_size
                    
                    output_path = output_dir / image_file.name
                    
                    if ImageOperations.compress_image(image_file, quality, output_path):
                        stats['successful'] += 1
                        stats['total_original_size'] += original_size
                        stats['total_new_size'] += output_path.stat().st_size
                    else:
                        stats['failed'] += 1
            
            if stats['total_original_size'] > 0:
                stats['compression_ratio'] = (
                    (stats['total_original_size'] - stats['total_new_size']) / 
                    stats['total_original_size'] * 100
                )
        except Exception as e:
            print(f"Error in batch compress: {e}")
        
        return stats
    
    @staticmethod
    def batch_convert(directory: Path, target_format: str, 
                     output_dir: Optional[Path] = None) -> Dict:
        """
        Convert all images in a directory to target format.
        """
        stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        try:
            output_dir = output_dir or directory / f'converted_{target_format}'
            output_dir.mkdir(exist_ok=True)
            
            for image_file in directory.glob('*'):
                if image_file.suffix.lower() in ImageOperations.SUPPORTED_FORMATS:
                    stats['total'] += 1
                    
                    output_path = output_dir / f"{image_file.stem}.{target_format}"
                    
                    if ImageOperations.convert_format(image_file, target_format, output_path):
                        stats['successful'] += 1
                    else:
                        stats['failed'] += 1
                        stats['errors'].append(str(image_file))
        except Exception as e:
            print(f"Error in batch convert: {e}")
        
        return stats
    
    @staticmethod
    def get_image_info(file_path: Path) -> Dict:
        """Get comprehensive image information."""
        try:
            image = Image.open(file_path)
            file_stat = file_path.stat()
            
            return {
                'filename': file_path.name,
                'format': image.format,
                'mode': image.mode,
                'width': image.width,
                'height': image.height,
                'size_bytes': file_stat.st_size,
                'size_mb': file_stat.st_size / (1024 * 1024),
                'dpi': image.info.get('dpi', (72, 72)),
                'has_animation': hasattr(image, 'n_frames') and image.n_frames > 1,
                'frame_count': getattr(image, 'n_frames', 1)
            }
        except Exception as e:
            print(f"Error getting image info: {e}")
            return {}
    
    @staticmethod
    def create_thumbnail(file_path: Path, thumb_size: Tuple[int, int] = (150, 150),
                        output_path: Optional[Path] = None) -> bool:
        """Create thumbnail for image."""
        try:
            image = Image.open(file_path)
            image.thumbnail(thumb_size, Image.Resampling.LANCZOS)
            
            save_path = output_path or file_path.parent / f".thumb_{file_path.name}"
            image.save(save_path)
            return True
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return False
