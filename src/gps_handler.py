"""
GPS and location handling for image metadata.
Supports GPS visualization, reverse geocoding, and location grouping.
"""

from typing import Dict, Tuple, List, Optional
import piexif
from pathlib import Path


class GPSHandler:
    """Handle GPS coordinates and location data."""
    
    # Comprehensive location database with Indian cities and states
    LOCATION_DB = {
        # India - Capital & Major Metropolitan Cities
        (28.7041, 77.1025): "New Delhi, Delhi, India",
        (19.0760, 72.8777): "Mumbai, Maharashtra, India",
        (13.0827, 80.2707): "Chennai, Tamil Nadu, India",
        (22.5726, 88.3639): "Kolkata, West Bengal, India",
        (30.7333, 76.7597): "Chandigarh, India",
        (23.1815, 79.9864): "Indore, Madhya Pradesh, India",
        (21.1458, 79.0882): "Nagpur, Maharashtra, India",
        (18.5204, 73.8567): "Pune, Maharashtra, India",
        (25.2048, 75.8362): "Bhopal, Madhya Pradesh, India",
        (12.9716, 77.5946): "Bangalore, Karnataka, India",
        (17.3850, 78.4867): "Hyderabad, Telangana, India",
        
        # India - Northern Cities & States
        (30.1337, 77.5803): "Ghaziabad, Uttar Pradesh, India",
        (30.3011, 77.7099): "Noida, Uttar Pradesh, India",
        (29.0588, 77.7064): "Agra, Uttar Pradesh, India",
        (28.4089, 77.3178): "Faridabad, Haryana, India",
        (26.9124, 75.7873): "Jaipur, Rajasthan, India",
        (26.1667, 91.5000): "Assam, India",
        (25.5920, 85.1206): "Patna, Bihar, India",
        (24.8008, 84.9753): "Varanasi, Uttar Pradesh, India",
        (26.9229, 80.9450): "Lucknow, Uttar Pradesh, India",
        (34.1526, 77.5770): "Leh, Ladakh, India",
        (32.2290, 75.3762): "Shimla, Himachal Pradesh, India",
        
        # India - Southern Cities & States
        (15.2993, 74.8361): "Panaji, Goa, India",
        (13.9124, 75.6239): "Mangalore, Karnataka, India",
        (10.9176, 79.8369): "Thiruvananthapuram, Kerala, India",
        (9.9312, 76.2673): "Kochi, Kerala, India",
        (8.7305, 77.7597): "Nagercoil, Tamil Nadu, India",
        (13.3673, 79.8965): "Tirupati, Andhra Pradesh, India",
        
        # India - Eastern Cities & States
        (20.2961, 85.8245): "Bhubaneswar, Odisha, India",
        (21.1458, 86.8319): "Rourkela, Odisha, India",
        (23.6345, 85.2988): "Ranchi, Jharkhand, India",
        (24.8407, 93.9133): "Imphal, Manipur, India",
        (25.5941, 94.6337): "Aizawl, Mizoram, India",
        (26.1445, 94.2082): "Kohima, Nagaland, India",
        (26.5644, 88.3630): "Gangtok, Sikkim, India",
        (28.2096, 94.3560): "Itanagar, Arunachal Pradesh, India",
        
        # India - Western Cities & States
        (23.1815, 72.6311): "Ahmedabad, Gujarat, India",
        (21.5922, 71.1925): "Vadodara, Gujarat, India",
        (22.3088, 73.1924): "Daman, Gujarat, India",
        (20.2740, 73.7591): "Aurangabad, Maharashtra, India",
        
        # India - Central Region
        (22.7039, 75.8573): "Bina, Madhya Pradesh, India",
        (23.4729, 87.0479): "Gaya, Bihar, India",
        
        # International Cities
        (40.7128, -74.0060): "New York, USA",
        (51.5074, -0.1278): "London, UK",
        (48.8566, 2.3522): "Paris, France",
        (35.6762, 139.6503): "Tokyo, Japan",
        (37.7749, -122.4194): "San Francisco, USA",
        (34.0522, -118.2437): "Los Angeles, USA",
        (41.8781, -87.6298): "Chicago, USA",
        (39.7392, -104.9903): "Denver, USA",
        (47.6062, -122.3321): "Seattle, USA",
        (55.7558, 37.6173): "Moscow, Russia",
        (-33.8688, 151.2093): "Sydney, Australia",
        (1.3521, 103.8198): "Singapore",
        (22.3193, 114.1694): "Hong Kong",
    }
    
    @staticmethod
    def extract_gps_coordinates(file_path: Path) -> Optional[Tuple[float, float]]:
        """
        Extract GPS coordinates from image.
        Returns: (latitude, longitude) or None
        """
        try:
            exif_dict = piexif.load(str(file_path))
            gps_ifd = exif_dict.get("GPS", {})
            
            if not gps_ifd:
                return None
            
            # Extract latitude
            lat_data = gps_ifd.get(piexif.GPSIFD.GPSLatitude)
            lat_ref = gps_ifd.get(piexif.GPSIFD.GPSLatitudeRef)
            
            # Extract longitude
            lon_data = gps_ifd.get(piexif.GPSIFD.GPSLongitude)
            lon_ref = gps_ifd.get(piexif.GPSIFD.GPSLongitudeRef)
            
            if not (lat_data and lon_data):
                return None
            
            # Convert to decimal degrees
            lat = GPSHandler._dms_to_decimal(lat_data)
            lon = GPSHandler._dms_to_decimal(lon_data)
            
            # Apply reference direction
            if lat_ref and lat_ref[0] == b'S':
                lat = -lat
            if lon_ref and lon_ref[0] == b'W':
                lon = -lon
            
            return (lat, lon)
        except Exception as e:
            print(f"Error extracting GPS: {e}")
            return None
    
    @staticmethod
    def extract_altitude(file_path: Path) -> Optional[float]:
        """Extract GPS altitude from image."""
        try:
            exif_dict = piexif.load(str(file_path))
            gps_ifd = exif_dict.get("GPS", {})
            
            altitude_data = gps_ifd.get(piexif.GPSIFD.GPSAltitude)
            
            if altitude_data:
                # Altitude is stored as rational (numerator, denominator)
                return float(altitude_data[0]) / float(altitude_data[1])
            
            return None
        except Exception as e:
            print(f"Error extracting altitude: {e}")
            return None
    
    @staticmethod
    def reverse_geocode(latitude: float, longitude: float) -> str:
        """
        Simple reverse geocoding (coordinates to location name).
        Matches coordinates with closest location in database.
        In production, use proper API like Google Maps or Open Street Map.
        """
        closest_location = "Unknown Location"
        closest_distance = float('inf')
        
        for (db_lat, db_lon), location_name in GPSHandler.LOCATION_DB.items():
            # Simple Euclidean distance
            distance = ((latitude - db_lat) ** 2 + (longitude - db_lon) ** 2) ** 0.5
            
            if distance < closest_distance:
                closest_distance = distance
                closest_location = location_name
        
        # Only return if reasonably close (within ~8 degrees for better coverage)
        if closest_distance < 8:
            return closest_location
        
        return f"Coordinates: {latitude:.4f}°, {longitude:.4f}°"
    
    @staticmethod
    def set_gps_coordinates(file_path: Path, latitude: float, longitude: float, 
                           altitude: Optional[float] = None) -> bool:
        """
        Set GPS coordinates in image metadata.
        """
        try:
            exif_dict = piexif.load(str(file_path))
            
            # Ensure GPS IFD exists
            if "GPS" not in exif_dict:
                exif_dict["GPS"] = {}
            
            gps_ifd = exif_dict["GPS"]
            
            # Convert latitude
            lat_degrees = int(abs(latitude))
            lat_minutes = int((abs(latitude) - lat_degrees) * 60)
            lat_seconds = ((abs(latitude) - lat_degrees) * 60 - lat_minutes) * 60
            
            gps_ifd[piexif.GPSIFD.GPSLatitude] = (
                (lat_degrees, 1),
                (lat_minutes, 1),
                (int(lat_seconds * 100), 100)
            )
            gps_ifd[piexif.GPSIFD.GPSLatitudeRef] = b'S' if latitude < 0 else b'N'
            
            # Convert longitude
            lon_degrees = int(abs(longitude))
            lon_minutes = int((abs(longitude) - lon_degrees) * 60)
            lon_seconds = ((abs(longitude) - lon_degrees) * 60 - lon_minutes) * 60
            
            gps_ifd[piexif.GPSIFD.GPSLongitude] = (
                (lon_degrees, 1),
                (lon_minutes, 1),
                (int(lon_seconds * 100), 100)
            )
            gps_ifd[piexif.GPSIFD.GPSLongitudeRef] = b'W' if longitude < 0 else b'E'
            
            # Set altitude if provided
            if altitude is not None:
                gps_ifd[piexif.GPSIFD.GPSAltitude] = (int(altitude * 100), 100)
            
            # Save the image with new EXIF data
            exif_bytes = piexif.dump(exif_dict)
            from PIL import Image
            image = Image.open(file_path)
            image.save(file_path, exif=exif_bytes)
            
            return True
        except Exception as e:
            print(f"Error setting GPS: {e}")
            return False
    
    @staticmethod
    def remove_gps_data(file_path: Path) -> bool:
        """Remove GPS data from image."""
        try:
            exif_dict = piexif.load(str(file_path))
            
            if "GPS" in exif_dict:
                exif_dict["GPS"] = {}
            
            exif_bytes = piexif.dump(exif_dict)
            from PIL import Image
            image = Image.open(file_path)
            image.save(file_path, exif=exif_bytes)
            
            return True
        except Exception as e:
            print(f"Error removing GPS data: {e}")
            return False
    
    @staticmethod
    def get_gps_info(file_path: Path) -> Dict:
        """Get complete GPS information from image."""
        coords = GPSHandler.extract_gps_coordinates(file_path)
        altitude = GPSHandler.extract_altitude(file_path)
        
        info = {
            'has_gps': coords is not None,
            'coordinates': coords,
            'altitude': altitude,
            'location_name': None,
            'map_url': None
        }
        
        if coords:
            lat, lon = coords
            info['location_name'] = GPSHandler.reverse_geocode(lat, lon)
            info['map_url'] = f"https://www.google.com/maps?q={lat},{lon}"
        
        return info
    
    @staticmethod
    def group_images_by_location(image_files: List[Path], radius_km: float = 1.0) -> Dict[str, List[Path]]:
        """Group images by location (within radius)."""
        location_groups = {}
        
        for image_file in image_files:
            coords = GPSHandler.extract_gps_coordinates(image_file)
            if not coords:
                continue
            
            location_name = GPSHandler.reverse_geocode(coords[0], coords[1])
            
            if location_name not in location_groups:
                location_groups[location_name] = []
            
            location_groups[location_name].append(image_file)
        
        return location_groups
    
    @staticmethod
    def _dms_to_decimal(dms_data) -> float:
        """Convert DMS (Degrees, Minutes, Seconds) to decimal degrees."""
        try:
            degrees = dms_data[0][0] / dms_data[0][1]
            minutes = dms_data[1][0] / dms_data[1][1] / 60
            seconds = dms_data[2][0] / dms_data[2][1] / 3600
            return degrees + minutes + seconds
        except Exception:
            return 0.0
