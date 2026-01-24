"""
Advanced tagging system for image metadata.
Supports custom tags, hierarchical structure, and tag suggestions.
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import Counter


class TaggingSystem:
    """Manage custom tags and tagging for images."""
    
    def __init__(self, tags_db_path: Optional[Path] = None):
        """Initialize tagging system with optional persistent storage."""
        self.tags_db_path = tags_db_path or Path.home() / '.metadata_expert' / 'tags.json'
        self.tags_db_path.parent.mkdir(parents=True, exist_ok=True)
        self.tags_hierarchy = {}
        self.image_tags = {}
        self.tag_history = []
        self.load_tags_db()
    
    def load_tags_db(self):
        """Load tags database from file."""
        try:
            if self.tags_db_path.exists():
                with open(self.tags_db_path, 'r') as f:
                    data = json.load(f)
                    self.tags_hierarchy = data.get('hierarchy', {})
                    self.image_tags = data.get('image_tags', {})
                    self.tag_history = data.get('history', [])
        except Exception as e:
            print(f"Error loading tags database: {e}")
    
    def save_tags_db(self):
        """Save tags database to file."""
        try:
            data = {
                'hierarchy': self.tags_hierarchy,
                'image_tags': self.image_tags,
                'history': self.tag_history[-1000:]  # Keep last 1000 entries
            }
            with open(self.tags_db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tags database: {e}")
    
    def add_tag(self, tag: str, category: str = 'General', description: str = ''):
        """Add a new tag to the hierarchy."""
        if category not in self.tags_hierarchy:
            self.tags_hierarchy[category] = {}
        
        self.tags_hierarchy[category][tag] = {
            'description': description,
            'count': 0,
            'created': str(Path.ctime(Path.cwd()))
        }
        self.save_tags_db()
    
    def add_tag_to_image(self, image_path: str, tag: str):
        """Add a tag to an image."""
        image_key = str(image_path)
        
        if image_key not in self.image_tags:
            self.image_tags[image_key] = []
        
        if tag not in self.image_tags[image_key]:
            self.image_tags[image_key].append(tag)
            self._update_tag_count(tag)
            self.tag_history.append({
                'action': 'add_tag',
                'image': image_key,
                'tag': tag,
                'timestamp': str(Path.ctime(Path.cwd()))
            })
            self.save_tags_db()
    
    def remove_tag_from_image(self, image_path: str, tag: str):
        """Remove a tag from an image."""
        image_key = str(image_path)
        
        if image_key in self.image_tags and tag in self.image_tags[image_key]:
            self.image_tags[image_key].remove(tag)
            self.tag_history.append({
                'action': 'remove_tag',
                'image': image_key,
                'tag': tag,
                'timestamp': str(Path.ctime(Path.cwd()))
            })
            self.save_tags_db()
    
    def get_image_tags(self, image_path: str) -> List[str]:
        """Get all tags for an image."""
        return self.image_tags.get(str(image_path), [])
    
    def get_tag_suggestions(self, partial_tag: str) -> List[str]:
        """Get autocomplete suggestions for tags."""
        suggestions = []
        partial_lower = partial_tag.lower()
        
        for category, tags in self.tags_hierarchy.items():
            for tag in tags.keys():
                if partial_lower in tag.lower():
                    suggestions.append(tag)
        
        # Sort by frequency
        suggestions.sort(key=lambda t: self._get_tag_count(t), reverse=True)
        return suggestions[:10]  # Return top 10
    
    def get_tag_cloud(self, limit: int = 50) -> Dict[str, int]:
        """Get tag cloud with frequency."""
        tag_counts = Counter()
        
        for tags in self.image_tags.values():
            for tag in tags:
                tag_counts[tag] += 1
        
        return dict(tag_counts.most_common(limit))
    
    def find_images_by_tag(self, tag: str) -> List[str]:
        """Find all images with a specific tag."""
        images = []
        for image_path, tags in self.image_tags.items():
            if tag in tags:
                images.append(image_path)
        return images
    
    def get_tag_statistics(self) -> Dict:
        """Get tagging statistics."""
        total_tags = sum(len(tags) for tags in self.image_tags.values())
        unique_tags = len(set(tag for tags in self.image_tags.values() for tag in tags))
        
        return {
            'total_images_tagged': len(self.image_tags),
            'total_tags_applied': total_tags,
            'unique_tags': unique_tags,
            'categories': list(self.tags_hierarchy.keys()),
            'most_common_tags': self.get_tag_cloud(10)
        }
    
    def _update_tag_count(self, tag: str):
        """Update tag count in hierarchy."""
        for category_tags in self.tags_hierarchy.values():
            if tag in category_tags:
                category_tags[tag]['count'] = category_tags[tag].get('count', 0) + 1
    
    def _get_tag_count(self, tag: str) -> int:
        """Get count for a tag."""
        for category_tags in self.tags_hierarchy.values():
            if tag in category_tags:
                return category_tags[tag].get('count', 0)
        return 0
    
    def export_tags_to_json(self, export_path: Path) -> bool:
        """Export tags to JSON file."""
        try:
            with open(export_path, 'w') as f:
                json.dump({
                    'hierarchy': self.tags_hierarchy,
                    'image_tags': self.image_tags,
                }, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting tags: {e}")
            return False
    
    def import_tags_from_json(self, import_path: Path) -> bool:
        """Import tags from JSON file."""
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
                self.tags_hierarchy.update(data.get('hierarchy', {}))
                self.image_tags.update(data.get('image_tags', {}))
                self.save_tags_db()
            return True
        except Exception as e:
            print(f"Error importing tags: {e}")
            return False
