"""UI components and layout functions"""

import streamlit as st
from src.config.settings import settings

def setup_page():
    """Setup page configuration and styling"""
    st.set_page_config(
        page_title=settings.APP_NAME,
        page_icon="📷",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS styling
    st.markdown("""
        <style>
        .main-header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .stSlider [data-baseweb="slider"] {
            background: #f0f2f6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 class='main-header'>{settings.APP_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>{settings.APP_DESCRIPTION}</p>", unsafe_allow_html=True)

def render_file_uploader():
    """Render file uploader component"""
    uploaded_file = st.file_uploader(
        "Upload an image file",
        type=settings.SUPPORTED_FORMATS,
        accept_multiple_files=False,
        key="image_uploader"
    )
    return uploaded_file

def render_augmentation_controls(preset_params=None):
    """Render all augmentation controls in sidebar"""
    if preset_params is None:
        preset_params = {}
    
    st.sidebar.header("🔧 Augmentation Controls")
    
    # Preset selection
    preset_options = ["Custom"] + [p['name'] for p in settings.PRESETS.values()]
    selected_preset = st.sidebar.selectbox(
        "Preset Configuration",
        preset_options,
        key="preset_selector"
    )
    
    st.sidebar.subheader("Geometric Transformations")
    
    rotation = st.sidebar.slider(
        "Rotation (degrees)",
        -180, 180,
        preset_params.get('rotation', settings.DEFAULT_VALUES['rotation']),
        key="rotation_slider"
    )
    
    flip_horizontal = st.sidebar.checkbox(
        "Flip Horizontal",
        preset_params.get('flip_horizontal', False),
        key="flip_h_checkbox"
    )
    
    flip_vertical = st.sidebar.checkbox(
        "Flip Vertical",
        preset_params.get('flip_vertical', False),
        key="flip_v_checkbox"
    )
    
    st.sidebar.subheader("Color Adjustments")
    
    brightness = st.sidebar.slider(
        "Brightness",
        0.1, 3.0,
        preset_params.get('brightness', settings.DEFAULT_VALUES['brightness']),
        key="brightness_slider"
    )
    
    contrast = st.sidebar.slider(
        "Contrast",
        0.1, 3.0,
        preset_params.get('contrast', settings.DEFAULT_VALUES['contrast']),
        key="contrast_slider"
    )
    
    saturation = st.sidebar.slider(
        "Saturation",
        0.1, 3.0,
        preset_params.get('saturation', settings.DEFAULT_VALUES['saturation']),
        key="saturation_slider"
    )
    
    sharpness = st.sidebar.slider(
        "Sharpness",
        0.1, 3.0,
        preset_params.get('sharpness', settings.DEFAULT_VALUES['sharpness']),
        key="sharpness_slider"
    )
    
    st.sidebar.subheader("Effects")
    
    gaussian_noise = st.sidebar.checkbox(
        "Gaussian Noise",
        preset_params.get('gaussian_noise', False),
        key="noise_checkbox"
    )
    
    gaussian_blur = st.sidebar.checkbox(
        "Gaussian Blur",
        preset_params.get('gaussian_blur', False),
        key="blur_checkbox"
    )
    
    motion_blur = st.sidebar.checkbox(
        "Motion Blur",
        preset_params.get('motion_blur', False),
        key="motion_blur_checkbox"
    )
    
    pixelate = st.sidebar.checkbox(
        "Pixelate",
        preset_params.get('pixelate', False),
        key="pixelate_checkbox"
    )
    
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

def render_image_comparison(original, augmented):
    """Render side-by-side image comparison"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖼️ Original Image")
        st.image(original, use_column_width=True)
    
    with col2:
        st.subheader("🎨 Augmented Image")
        st.image(augmented, use_column_width=True)

def render_download_button(augmented_image):
    """Render download button for augmented image"""
    import io
    
    buf = io.BytesIO()
    augmented_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="💾 Download Augmented Image",
        data=byte_im,
        file_name="augmented_image.png",
        mime="image/png",
        key="download_btn"
    )