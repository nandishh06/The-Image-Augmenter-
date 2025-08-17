"""Batch image generation engine - creates multiple augmented versions from single image"""

import os
import random
import time
from pathlib import Path
from PIL import Image
from src.core.image_processor import ImageProcessor
from src.utils.helpers import validate_file_format

class BatchGenerator:
    """Generate multiple augmented versions from a single image"""
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.settings = self.processor.settings
    
    def generate_batch(self, original_image, count, output_folder, base_name="augmented", progress_callback=None):
        """Generate multiple augmented versions of a single image"""
        
        # Create output folder if it doesn't exist
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        generated_count = 0
        failed_count = 0
        failed_files = []
        
        # Generate specified number of images
        for i in range(count):
            try:
                # Call progress callback
                if progress_callback:
                    progress_callback(i + 1, count, f"{base_name}_{i+1:04d}.png")
                
                # Generate random augmentations
                augmentation_params = self._generate_random_params()
                
                # Apply transformations
                augmented_image = self.processor.apply_transformations(original_image, augmentation_params)
                
                # Save augmented image
                filename = f"{base_name}_{i+1:04d}.png"
                output_path = Path(output_folder) / filename
                augmented_image.save(output_path, format="PNG")
                
                generated_count += 1
                
            except Exception as e:
                failed_count += 1
                failed_files.append((f"{base_name}_{i+1:04d}.png", str(e)))
                print(f"Failed to generate {base_name}_{i+1:04d}.png: {str(e)}")
        
        return {
            'requested': count,
            'generated': generated_count,
            'failed': failed_count,
            'failed_files': failed_files
        }
    
    def _generate_random_params(self):
        """Generate random augmentation parameters"""
        # Geometric transformations
        rotation = random.randint(-30, 30)  # -30 to 30 degrees
        flip_horizontal = random.choice([True, False])
        flip_vertical = random.choice([True, False])
        
        # Color adjustments
        brightness = round(random.uniform(0.7, 1.3), 2)  # 0.7 to 1.3
        contrast = round(random.uniform(0.8, 1.2), 2)    # 0.8 to 1.2
        saturation = round(random.uniform(0.7, 1.3), 2)  # 0.7 to 1.3
        sharpness = round(random.uniform(0.8, 1.2), 2)   # 0.8 to 1.2
        
        # Effects (30% chance each)
        gaussian_noise = random.random() < 0.3
        gaussian_blur = random.random() < 0.2
        motion_blur = random.random() < 0.1
        pixelate = random.random() < 0.15
        
        return {
            'rotation': rotation,
            'flip_horizontal': flip_horizontal,
            'flip_vertical': flip_vertical,
            'brightness': brightness,
            'contrast': contrast,
            'saturation': saturation,
            'sharpness': sharpness,
            'gaussian_noise': gaussian_noise,
            'gaussian_blur': gaussian_blur,
            'motion_blur': motion_blur,
            'pixelate': pixelate
        }
    
    def generate_with_preset(self, original_image, count, output_folder, preset_type, base_name="augmented", progress_callback=None):
        """Generate batch with specific preset variations"""
        
        # Create output folder if it doesn't exist
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        generated_count = 0
        failed_count = 0
        failed_files = []
        
        # Get preset parameters
        preset_params = self.processor.get_preset_params(preset_type)
        
        # Generate specified number of images
        for i in range(count):
            try:
                # Call progress callback
                if progress_callback:
                    progress_callback(i + 1, count, f"{base_name}_{i+1:04d}.png")
                
                # Apply some random variation to preset
                augmentation_params = self._vary_preset_params(preset_params, i)
                
                # Apply transformations
                augmented_image = self.processor.apply_transformations(original_image, augmentation_params)
                
                # Save augmented image
                filename = f"{base_name}_{i+1:04d}.png"
                output_path = Path(output_folder) / filename
                augmented_image.save(output_path, format="PNG")
                
                generated_count += 1
                
            except Exception as e:
                failed_count += 1
                failed_files.append((f"{base_name}_{i+1:04d}.png", str(e)))
                print(f"Failed to generate {base_name}_{i+1:04d}.png: {str(e)}")
        
        return {
            'requested': count,
            'generated': generated_count,
            'failed': failed_count,
            'failed_files': failed_files
        }
    
    def _vary_preset_params(self, preset_params, seed):
        """Add random variations to preset parameters"""
        import random
        random.seed(seed)  # For reproducible variations
        
        varied_params = preset_params.copy()
        
        # Add small random variations
        if 'rotation' in varied_params:
            varied_params['rotation'] += random.randint(-10, 10)
            varied_params['rotation'] = max(-180, min(180, varied_params['rotation']))
        
        if 'brightness' in varied_params:
            varied_params['brightness'] *= random.uniform(0.9, 1.1)
            varied_params['brightness'] = max(0.1, min(3.0, varied_params['brightness']))
        
        if 'contrast' in varied_params:
            varied_params['contrast'] *= random.uniform(0.95, 1.05)
            varied_params['contrast'] = max(0.1, min(3.0, varied_params['contrast']))
        
        if 'saturation' in varied_params:
            varied_params['saturation'] *= random.uniform(0.9, 1.1)
            varied_params['saturation'] = max(0.1, min(3.0, varied_params['saturation']))
        
        if 'sharpness' in varied_params:
            varied_params['sharpness'] *= random.uniform(0.95, 1.05)
            varied_params['sharpness'] = max(0.1, min(3.0, varied_params['sharpness']))
        
        return varied_params

class GenerationProgress:
    """Progress tracking for batch generation"""
    
    def __init__(self):
        self.current = 0
        self.total = 0
        self.current_file = ""
    
    def update(self, current, total, filename):
        """Update progress"""
        self.current = current
        self.total = total
        self.current_file = filename
        self._print_progress()
    
    def _print_progress(self):
        """Print progress to console"""
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        print(f"\rGenerating: {self.current}/{self.total} ({percentage:.1f}%) - {self.current_file}", end='', flush=True)