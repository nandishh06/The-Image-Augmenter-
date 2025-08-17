"""Application configuration and settings"""

class Settings:
    # App metadata
    APP_NAME = "Image Augmenter"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Professional Image Augmentation Tool"
    
    # Supported formats
    SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'bmp', 'tiff']
    
    # Processing limits
    MAX_IMAGE_SIZE = 2000  # pixels
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Default augmentation values
    DEFAULT_VALUES = {
        'rotation': 0,
        'brightness': 1.0,
        'contrast': 1.0,
        'saturation': 1.0,
        'sharpness': 1.0
    }
    
    # Preset configurations
    PRESETS = {
        'ml_training': {
            'name': 'ML Training',
            'rotation': 15,
            'flip_horizontal': True,
            'brightness': 1.2,
            'contrast': 1.1,
            'gaussian_noise': True
        },
        'creative': {
            'name': 'Creative',
            'saturation': 1.5,
            'sharpness': 1.3,
            'pixelate': True
        },
        'enhancement': {
            'name': 'Enhancement',
            'brightness': 1.1,
            'contrast': 1.2,
            'sharpness': 1.2
        }
    }

# Global settings instance
settings = Settings()