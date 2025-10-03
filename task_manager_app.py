"""
Task Manager - Streamlit Web Application

This is the main Streamlit application that provides a beautiful web interface
for managing tasks in either a Notion database or SQLite database. Users can create,
view, edit, update, and delete tasks with real-time synchronization.

Features:
    - Add new tasks with custom status
    - Filter tasks by status (All, Not started, In progress, Done)
    - Edit task names inline
    - Update task status with dropdown selectors
    - Delete (archive) tasks
    - Visual status icons and metrics dashboard
    - Beautiful gradient UI with custom styling
    - Switch between Notion and SQLite backends

Dependencies:
    - streamlit: Web application framework
    - task_manager_helper: Task management helper functions
    - style_helper: Custom CSS and JavaScript styling

Configuration:
    For Notion backend, requires Streamlit secrets in .streamlit/secrets.toml:
    - NOTION_AUTH_TOKEN: Notion API authentication token
    - NOTION_DATABASE_ID: Target Notion database ID
    
    Example .streamlit/secrets.toml:
        NOTION_AUTH_TOKEN = "secret_xxxxxxxxxxxxx"
        NOTION_DATABASE_ID = "xxxxxxxxxxxxx"
    
    For SQLite backend, uses local tasks.db file (created automatically)

Usage:
    streamlit run notion_streamlit.py
"""

import streamlit as st
from style_helper import StyleHelper
from task_manager_helper import TaskManagerHelper
import time

# Page configuration
st.set_page_config(
    page_title="Task Manager",
    page_icon="📋",
    layout="wide"
)

# Initialize StyleHelper and apply all styling
style_helper = StyleHelper()
style_helper.apply_all_styling()

# Sidebar for database selection
with st.sidebar:
    database_backend = TaskManagerHelper.show_sidebar_settings()

# Main app header
TaskManagerHelper.show_app_header(database_backend)

# Initialize task manager
task_manager = TaskManagerHelper.get_task_manager(database_backend)
TaskManagerHelper.show_add_task_form(task_manager)

# Status filter
status_filter = TaskManagerHelper.show_status_filter()

# Fetch tasks
tasks = TaskManagerHelper.fetch_tasks(task_manager, status_filter)

# Check if tasks is None (error) or just empty list (no tasks)
if tasks is not None:
    if tasks:
        # Display task list
        TaskManagerHelper.show_task_list(tasks, task_manager, style_helper, database_backend)
        # Show summary
        TaskManagerHelper.show_task_summary(tasks, status_filter, style_helper)
    else:
        # Empty list - no tasks yet
        st.info("📝 No tasks yet. Add your first task above!")
        
else:
    # tasks is None - error occurred
    st.error("❌ Error loading tasks. Please check your database connection.")

# Footer buttons
TaskManagerHelper.show_footer_buttons(database_backend, tasks, task_manager, status_filter)
