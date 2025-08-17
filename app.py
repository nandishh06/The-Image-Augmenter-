"""Main Streamlit application"""

import streamlit as st
from src.ui.components import setup_page
from src.ui.generator_components import render_generation_interface, render_generation_tips

def main():
    """Main application function"""
    
    # Setup page
    setup_page()
    
    # Add custom CSS for better UI
    st.markdown("""
        <style>
        .stProgress > div > div > div {
            background-color: #667eea;
        }
        .metric-value {
            font-size: 2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Render generation interface
    render_generation_tips()
    render_generation_interface()

if __name__ == "__main__":
    main()