"""Main image processing controller"""

from PIL import Image
from src.core.augmentations import AugmentationEngine
from src.utils.helpers import validate_file_format, resize_if_needed, validate_file_size
from src.config.settings import settings

class ImageProcessor:
    """Main image processing controller"""
    
    def __init__(self):
        self.engine = AugmentationEngine()
        self.settings = settings
    
    def load_and_validate_image(self, file_obj):
        """Load and validate image file"""
        # Validate file format
        if not validate_file_format(file_obj.name, self.settings.SUPPORTED_FORMATS):
            raise ValueError(f"Unsupported file format. Supported: {self.settings.SUPPORTED_FORMATS}")
        
        # Validate file size
        if not validate_file_size(file_obj, self.settings.MAX_FILE_SIZE):
            raise ValueError(f"File too large. Maximum size: {self.settings.MAX_FILE_SIZE//1024//1024}MB")
        
        # Load image
        try:
            image = Image.open(file_obj)
            return resize_if_needed(image, self.settings.MAX_IMAGE_SIZE)
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")
    
    def apply_transformations(self, image, params):
        """Apply all selected transformations"""
        result = image.copy()
        
        # Geometric transformations
        if params.get('rotation', 0) != 0:
            result = self.engine.rotate(result, params['rotation'])
        
        if params.get('flip_horizontal'):
            result = self.engine.flip_horizontal(result)
        
        if params.get('flip_vertical'):
            result = self.engine.flip_vertical(result)
        
        # Color adjustments
        if params.get('brightness', 1.0) != 1.0:
            result = self.engine.adjust_brightness(result, params['brightness'])
        
        if params.get('contrast', 1.0) != 1.0:
            result = self.engine.adjust_contrast(result, params['contrast'])
        
        if params.get('saturation', 1.0) != 1.0:
            result = self.engine.adjust_saturation(result, params['saturation'])
        
        if params.get('sharpness', 1.0) != 1.0:
            result = self.engine.adjust_sharpness(result, params['sharpness'])
        
        # Effects
        if params.get('gaussian_noise'):
            result = self.engine.add_gaussian_noise(result)
        
        if params.get('gaussian_blur'):
            result = self.engine.gaussian_blur(result)
        
        if params.get('motion_blur'):
            result = self.engine.motion_blur(result)
        
        if params.get('pixelate'):
            result = self.engine.pixelate(result)
        
        return result
    
    def get_preset_params(self, preset_name):
        """Get parameters for a preset configuration"""
        preset = self.settings.PRESETS.get(preset_name.lower())
        return preset.copy() if preset else {}