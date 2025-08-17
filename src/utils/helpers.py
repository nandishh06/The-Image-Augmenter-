"""Utility functions for image processing"""

import numpy as np
from PIL import Image
import cv2
import os

def pil_to_cv2(pil_image):
    """Convert PIL Image to OpenCV format"""
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv2_image):
    """Convert OpenCV image to PIL format"""
    return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))

def validate_file_format(filename, supported_formats):
    """Check if file format is supported"""
    if not filename:
        return False
    extension = os.path.splitext(filename.lower())[1][1:]
    return extension in supported_formats

def resize_if_needed(image, max_size):
    """Resize image if it exceeds maximum dimensions"""
    width, height = image.size
    if width > max_size or height > max_size:
        ratio = min(max_size/width, max_size/height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return image

def validate_file_size(file_obj, max_size):
    """Check if file size is within limits"""
    file_obj.seek(0, 2)  # Seek to end
    file_size = file_obj.tell()
    file_obj.seek(0)  # Reset to beginning
    return file_size <= max_size