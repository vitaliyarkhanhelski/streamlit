"""
Style Helper Module for Streamlit Applications

This module provides utility classes and methods for managing custom styling
in Streamlit applications. It handles loading external CSS files, injecting
JavaScript for dynamic UI behaviors, and creating custom styled components.

Classes:
    StyleHelper: Main utility class for styling management

Key Features:
    - Load and apply external CSS files
    - Inject JavaScript for button hover animations
    - Create custom styled components (metrics, status icons)
    - Apply inline CSS and JavaScript dynamically
    - DOM mutation observer for dynamic content updates

Components:
    - Bordered metrics dashboard with task statistics
    - Status icons with color coding (✅ Done, ⏳ In Progress, ⭕ Not Started)
    - Button scaling animations via JavaScript event listeners

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
    Helper class to manage CSS and JavaScript styling for Streamlit applications.
    
    This class provides methods to load external stylesheets, apply custom CSS,
    inject JavaScript for dynamic behaviors, and create pre-styled UI components
    like metrics dashboards and status icons.
    
    Attributes:
        css_file (str): Path to the external CSS file to load
    
    Methods:
        load_css_file: Load CSS content from external file
        apply_css: Apply CSS styling to the app
        apply_button_scaling_js: Add JavaScript for button hover effects
        apply_all_styling: Apply both CSS and JavaScript styling
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
    
    def apply_css(self):
        """Apply CSS styling to the Streamlit app"""
        css_content = self.load_css_file()
        if css_content:
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    
    def apply_button_scaling_js(self):
        """Apply JavaScript for button scaling effects"""
        js_code = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Function to add hover scaling to buttons
            function addButtonScaling() {
                console.log('Adding button scaling...');
                
                // Target ALL buttons as ultimate fallback
                const allButtons = document.querySelectorAll('button');
                console.log('Found', allButtons.length, 'buttons');
                
                allButtons.forEach((button, index) => {
                    // Remove existing listeners to avoid duplicates
                    button.removeEventListener('mouseenter', button._mouseEnterHandler);
                    button.removeEventListener('mouseleave', button._mouseLeaveHandler);
                    
                    // Create new handlers
                    button._mouseEnterHandler = function() {
                        console.log('Button hover:', this.textContent);
                        this.style.transform = 'scale(1.1)';
                        this.style.transition = 'all 0.3s ease';
                    };
                    
                    button._mouseLeaveHandler = function() {
                        this.style.transform = 'scale(1)';
                    };
                    
                    // Add event listeners
                    button.addEventListener('mouseenter', button._mouseEnterHandler);
                    button.addEventListener('mouseleave', button._mouseLeaveHandler);
                });
                
                // Specific targeting for different button types
                const primaryButtons = document.querySelectorAll('.stButton button[kind="primary"]');
                const formButtons = document.querySelectorAll('.stForm .stButton button');
                const secondaryButtons = document.querySelectorAll('.stButton button[kind="secondary"]');
                
                console.log('Primary buttons:', primaryButtons.length);
                console.log('Form buttons:', formButtons.length);
                console.log('Secondary buttons:', secondaryButtons.length);
            }
            
            // Run immediately and on any updates
            addButtonScaling();
            
            // Re-run when Streamlit updates the DOM
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'childList') {
                        addButtonScaling();
                    }
                });
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        });
        </script>
        """
        st.markdown(js_code, unsafe_allow_html=True)
    
    def apply_all_styling(self):
        """Apply both CSS and JavaScript styling"""
        self.apply_css()
        self.apply_button_scaling_js()
    
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