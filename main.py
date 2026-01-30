#!/usr/bin/env python3
"""
Metadata Viewer - Main Entry Point
Cross-platform GUI application for viewing image metadata
"""

import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from metadata_viewer import main
    main()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

