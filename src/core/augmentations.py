"""Image augmentation functions"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from src.utils.helpers import pil_to_cv2, cv2_to_pil

class AugmentationEngine:
    """Core image augmentation engine"""
    
    @staticmethod
    def rotate(image, angle):
        """Rotate image by angle degrees"""
        if angle == 0:
            return image
        image_cv = pil_to_cv2(image)
        (h, w) = image_cv.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image_cv, matrix, (w, h))
        return cv2_to_pil(rotated)
    
    @staticmethod
    def flip_horizontal(image):
        """Flip image horizontally"""
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    
    @staticmethod
    def flip_vertical(image):
        """Flip image vertically"""
        return image.transpose(Image.FLIP_TOP_BOTTOM)
    
    @staticmethod
    def adjust_brightness(image, factor):
        """Adjust image brightness"""
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_contrast(image, factor):
        """Adjust image contrast"""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_saturation(image, factor):
        """Adjust image saturation"""
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_sharpness(image, factor):
        """Adjust image sharpness"""
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def add_gaussian_noise(image, sigma=15):
        """Add Gaussian noise to image"""
        image_cv = pil_to_cv2(image)
        row, col, ch = image_cv.shape
        mean = 0
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy = image_cv + gauss
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)
        return cv2_to_pil(noisy)
    
    @staticmethod
    def gaussian_blur(image, kernel_size=5):
        """Apply Gaussian blur"""
        return image.filter(ImageFilter.GaussianBlur(radius=kernel_size//2))
    
    @staticmethod
    def motion_blur(image, size=15):
        """Apply motion blur"""
        image_cv = pil_to_cv2(image)
        kernel_motion_blur = np.zeros((size, size))
        kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
        kernel_motion_blur = kernel_motion_blur / size
        blurred = cv2.filter2D(image_cv, -1, kernel_motion_blur)
        return cv2_to_pil(blurred)
    
    @staticmethod
    def pixelate(image, pixel_size=5):
        """Apply pixelation effect"""
        small = image.resize(
            (image.width // pixel_size, image.height // pixel_size),
            Image.NEAREST
        )
        return small.resize(image.size, Image.NEAREST)