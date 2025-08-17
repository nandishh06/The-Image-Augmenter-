"""Batch generation UI components"""

import streamlit as st
import os
from pathlib import Path
from src.core.batch_generator import BatchGenerator, GenerationProgress
from src.ui.components import render_augmentation_controls

def render_generation_interface():
    """Render batch generation interface"""
    st.header("⚡ Batch Generation")
    st.markdown("Generate multiple augmented versions from a single image")
    
    # File uploader for base image
    uploaded_file = st.file_uploader(
        "Upload base image to generate variations",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        key="generator_uploader"
    )
    
    if uploaded_file is not None:
        try:
            # Initialize generator
            generator = BatchGenerator()
            
            # Load and validate image
            original_image = generator.processor.load_and_validate_image(uploaded_file)
            
            st.success("✅ Image loaded successfully!")
            st.image(original_image, caption="Base Image", width=300)
            
            # Generation settings
            st.subheader("⚙️ Generation Settings")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                count = st.number_input(
                    "Number of Images",
                    min_value=1,
                    max_value=1500,
                    value=10,
                    step=10,
                    key="gen_count"
                )
            
            with col2:
                base_name = st.text_input(
                    "Base Filename",
                    value="augmented",
                    key="gen_basename"
                )
            
            with col3:
                preset_type = st.selectbox(
                    "Generation Preset",
                    ["Random", "ML Training", "Creative", "Enhancement"],
                    key="gen_preset"
                )
            
            # Output folder
            output_folder = st.text_input(
                "Output Folder Path",
                value=str(Path.home() / "Desktop" / "augmented_images"),
                key="gen_output_folder"
            )
            
            # Create output folder button
            if st.button("📁 Create Output Folder"):
                try:
                    Path(output_folder).mkdir(parents=True, exist_ok=True)
                    st.success("✅ Output folder created!")
                except Exception as e:
                    st.error(f"❌ Failed to create folder: {str(e)}")
            
            # Show folder info
            if os.path.exists(output_folder):
                st.info(f"📁 Output folder: {output_folder}")
            else:
                st.warning("⚠️ Output folder doesn't exist yet")
            
            # Generate button
            if st.button("🚀 Generate Images", key="generate_btn", type="primary", use_container_width=True):
                if not os.path.exists(output_folder):
                    st.error("❌ Output folder does not exist. Please create it first.")
                    return
                
                try:
                    # Show processing message
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def progress_callback(current, total, filename):
                        progress = current / total
                        progress_bar.progress(progress)
                        status_text.info(f"Generating {current}/{total}: {filename}")
                    
                    # Generate batch
                    with st.spinner("Generating images..."):
                        if preset_type == "Random":
                            result = generator.generate_batch(
                                original_image,
                                count,
                                output_folder,
                                base_name,
                                progress_callback
                            )
                        else:
                            result = generator.generate_with_preset(
                                original_image,
                                count,
                                output_folder,
                                preset_type.lower().replace(" ", "_"),
                                base_name,
                                progress_callback
                            )
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Show results
                    st.success("✅ Generation complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Requested", result['requested'])
                    col2.metric("Generated", result['generated'])
                    col3.metric("Failed", result['failed'])
                    
                    if result['failed'] > 0:
                        st.warning(f"{result['failed']} images failed to generate")
                        if st.checkbox("Show failed files"):
                            for filename, error in result['failed_files']:
                                st.text(f"• {filename}: {error}")
                    
                    # Open folder button
                    if st.button("📂 Open Output Folder"):
                        try:
                            import subprocess
                            import platform
                            
                            if platform.system() == "Windows":
                                os.startfile(output_folder)
                            elif platform.system() == "Darwin":  # macOS
                                subprocess.call(["open", output_folder])
                            else:  # Linux
                                subprocess.call(["xdg-open", output_folder])
                        except Exception as e:
                            st.error(f"Could not open folder: {str(e)}")
                    
                    # Download summary
                    summary_text = f"""
Batch Generation Summary:
- Base image: {uploaded_file.name}
- Requested images: {result['requested']}
- Successfully generated: {result['generated']}
- Failed: {result['failed']}
- Output folder: {output_folder}
- Preset used: {preset_type}
                    """
                    
                    st.download_button(
                        label="📥 Download Summary",
                        data=summary_text,
                        file_name="generation_summary.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Generation failed: {str(e)}")
                    st.info("💡 Try reducing the number of images or checking the output folder path.")
            
            # Show example
            with st.expander("💡 Example Usage"):
                st.markdown("""
                **To generate 1500 images:**
                1. Upload your base image
                2. Set "Number of Images" to 1500
                3. Choose a preset (or Random for varied results)
                4. Set output folder (e.g., `C:/Users/YourName/Desktop/augmented_images`)
                5. Click "Create Output Folder"
                6. Click "Generate Images"
                
                **Tips:**
                - Start with smaller numbers (10-50) for testing
                - "ML Training" preset is good for dataset augmentation
                - "Creative" preset creates more artistic variations
                - Generation may take several minutes for large batches
                """)
                
        except Exception as e:
            st.error(f"❌ Error loading image: {str(e)}")
    else:
        st.info("👆 Please upload an image to start generating variations")

def render_generation_tips():
    """Render generation tips and best practices"""
    with st.expander("📚 Tips for Best Results", expanded=False):
        st.markdown("""
        ### Generation Presets:
        - **Random**: Completely random augmentations
        - **ML Training**: Good for machine learning datasets
        - **Creative**: Artistic and varied results
        - **Enhancement**: Subtle improvements to images
        
        ### Performance Tips:
        - High-resolution images take longer to process
        - Consider generating in batches of 100-500 for large sets
        - Ensure enough disk space (estimate 1-5MB per image)
        - Close other applications during generation
        
        ### Output Organization:
        - Files are named: `basename_0001.png`, `basename_0002.png`, etc.
        - All files are saved in PNG format for quality
        - Output folder is created automatically if it doesn't exist
        """)