"""
Style Helper Module for Streamlit Applications

This module provides utility classes and methods for managing custom styling
in Streamlit applications. It handles loading external CSS files and creating
custom styled components.

Classes:
    StyleHelper: Main utility class for styling management

Key Features:
    - Load and apply external CSS files
    - Create custom styled components (metrics, status icons)
    - Apply inline CSS and JavaScript dynamically

Components:
    - Bordered metrics dashboard with task statistics
    - Status icons with color coding (✅ Done, ⏳ In Progress, ⭕ Not Started)

Usage:
    from style_helper import StyleHelper
    
    style_helper = StyleHelper("styles.css")
    style_helper.apply_all_styling()
    style_helper.create_status_icon("Done")
    style_helper.create_bordered_metrics(total_tasks=10, in_progress=3, not_started=2, done=5)
"""

import streamlit as st
import os


class StyleHelper:
    """
    Helper class to manage CSS styling for Streamlit applications.
    
    This class provides methods to load external stylesheets, apply custom CSS,
    and create pre-styled UI components like metrics dashboards and status icons.
    
    Attributes:
        css_file (str): Path to the external CSS file to load
    
    Methods:
        load_css_file: Load CSS content from external file
        apply_css: Apply CSS styling to the app
        apply_all_styling: Apply CSS styling to the app
        create_custom_css: Static method to apply inline CSS
        create_custom_js: Static method to apply inline JavaScript
        create_bordered_metrics: Static method to create metrics dashboard
        create_status_icon: Static method to create status icon
    """
    
    def __init__(self, css_file="styles.css"):
        self.css_file = css_file
    
    def load_css_file(self):
        """Load CSS from external file"""
        try:
            if os.path.exists(self.css_file):
                with open(self.css_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                st.warning(f"CSS file '{self.css_file}' not found. Using default styling.")
                return ""
        except Exception as e:
            st.error(f"Error loading CSS file: {e}")
            return ""
    
    def apply_css(self, database_backend=None):
        """Apply CSS styling to the Streamlit app with optional backend-specific background"""
        css_content = self.load_css_file()
        if css_content:
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        
        # Apply backend-specific background gradient
        if database_backend:
            # Define color variables for each backend
            if database_backend == "Notion":
                color_start = "#ccc9fd"  # Notion - slightly warmer/pinker
                color_end = "#d5c7e8"
            else:  # SQLite
                color_start = "#bfcbff"  # SQLite - more blue/cooler purple
                color_end = "#c8bfeb"
            
            # Apply gradient with interpolated colors
            background_css = f"""
            <style>
            .stApp {{
                background: linear-gradient(135deg, {color_start} 0%, {color_end} 100%) !important;
                min-height: 100vh;
            }}
            </style>
            """
            st.markdown(background_css, unsafe_allow_html=True)
    
    def apply_all_styling(self, database_backend=None):
        """Apply CSS styling with optional backend-specific customization"""
        self.apply_css(database_backend)
    
    @staticmethod
    def create_custom_css(css_rules):
        """Apply custom CSS rules directly"""
        st.markdown(f"<style>{css_rules}</style>", unsafe_allow_html=True)
    
    @staticmethod
    def create_custom_js(js_code):
        """Apply custom JavaScript directly"""
        st.markdown(js_code, unsafe_allow_html=True)
    
    @staticmethod
    def create_bordered_metrics(total_tasks, in_progress, not_started, done, 
                               border_color="#9394cd", font_size="2.5rem", 
                               label_color="#000000", value_color="#000"):
        """Create bordered metrics display with custom styling"""
        metrics_html = f"""
        <div style="border: 1px solid {border_color}; border-radius: 8px; padding: 10px; margin: 20px 0; background-color: transparent; box-sizing: border-box; display: flex; justify-content: space-around; align-items: center; margin-bottom: 30px;">
            <div style="text-align: center;">
                <div style="font-size: 0.875rem; color: {label_color}; margin-bottom: 0rem;">Total Tasks</div>
                <div style="font-size: {font_size}; font-weight: 600; color: {value_color};">{total_tasks}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 0.875rem; color: {label_color}; margin-bottom: 0rem;">In Progress</div>
                <div style="font-size: {font_size}; font-weight: 600; color: {value_color};">{in_progress}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 0.875rem; color: {label_color}; margin-bottom: 0rem;">Not Started</div>
                <div style="font-size: {font_size}; font-weight: 600; color: {value_color};">{not_started}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 0.875rem; color: {label_color}; margin-bottom: 0rem;">Done</div>
                <div style="font-size: {font_size}; font-weight: 600; color: {value_color};">{done}</div>
            </div>
        </div>
        """
        st.markdown(metrics_html, unsafe_allow_html=True)
    
    @staticmethod
    def create_status_icon(status, font_size="1.5rem"):
        """Create a status icon based on task status"""
        if status == "Done":
            icon_html = f'<div style="text-align: center; font-size: {font_size}; color: #28a745;">✅</div>'
        elif status == "In progress":
            icon_html = f'<div style="text-align: center; font-size: {font_size}; color: #007bff;">⏳</div>'
        else:  # Not started
            icon_html = f'<div style="text-align: center; font-size: {font_size}; color: #6c757d;">⭕</div>'
        
        st.markdown(icon_html, unsafe_allow_html=True)