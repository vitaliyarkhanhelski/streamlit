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
    - pandas: Data manipulation
    - notion_manager: Notion API integration
    - sql_manager: SQLite database integration
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
import pandas as pd
from notion_manager import NotionTaskManager
from sql_manager import SqlTaskManager
from style_helper import StyleHelper

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
    st.header("⚙️ Settings")
    database_backend = st.radio(
        "Choose Database Backend:",
        ["SQLite", "Notion"],
        index=0,
        help="Select which database to use for storing tasks"
    )
    
    st.markdown("---")
    
    if database_backend == "Notion":
        st.info("🔗 Using Notion API")
        st.caption("Requires configuration in .streamlit/secrets.toml")
    else:
        st.info("💾 Using Local SQLite")
        st.caption("Data stored in tasks.db file")

# Initialize task manager
@st.cache_resource
def get_task_manager(backend):
    """
    Get the appropriate task manager based on the selected backend.
    
    Args:
        backend (str): Either "Notion" or "SQLite"
    
    Returns:
        NotionTaskManager or SqlTaskManager instance
    """
    if backend == "Notion":
        try:
            auth_token = st.secrets["NOTION_AUTH_TOKEN"]
            database_id = st.secrets["NOTION_DATABASE_ID"]
            return NotionTaskManager(auth_token, database_id)
        except Exception as e:
            st.error(f"❌ Notion configuration error: {e}")
            st.info("💡 Falling back to SQLite. Please configure Notion secrets to use Notion backend.")
            return SqlTaskManager()
    else:
        return SqlTaskManager()

# Main app
backend_icon = "🔗" if database_backend == "Notion" else "💾"
st.title(f"📋 Task Manager {backend_icon} {database_backend}")
st.markdown("---")

# Initialize task manager
task_manager = get_task_manager(database_backend)

st.subheader("➕ Add New Task")

# Form for adding a task
with st.form("add_task_form", clear_on_submit=True):
    task_name = st.text_input("Task Name:", placeholder="Enter task name...")
    task_status = st.selectbox("Status:", ["Not started", "In progress", "Done"])

    submitted = st.form_submit_button("Add Task", type="primary")

    if submitted:
        # Validate task name
        if not task_name.strip():
            st.error("❌ Please provide a task name.")
        else:
            with st.spinner("Adding task..."):
                result = task_manager.add_task(task_name, task_status)
                if result:
                    st.success(f"✅ Task '{task_name}' added successfully!")
                    st.toast("🎉 Task added successfully!", icon="✅")
                else:
                    st.error("❌ Failed to add task.")
                    st.toast("❌ Failed to add task", icon="⚠️")

# Status filter
st.subheader("🔍 Filter Tasks")
status_filter = st.selectbox(
    "Filter by status:",
    ["All", "Not started", "In progress", "Done"],
    index=0
)

# Fetch tasks
with st.spinner("Loading tasks..."):
    if status_filter == "All":
        tasks = task_manager.list_tasks()
    else:
        tasks = task_manager.list_tasks(status_filter)

if tasks:
    # Convert to DataFrame
    df = pd.DataFrame(tasks)
    
    # Display the table with delete buttons
    st.markdown("<h3 style='text-align: center;'>📊 All Tasks</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    for task in tasks:
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        with col1:
            # Show task name as text
            st.write(f"**{task['name']}**")
        with col2:
            # Edit button
            if st.button("Edit", key=f"edit_{task['id']}", help="Edit task name", type="secondary"):
                st.session_state[f"editing_{task['id']}"] = True
                st.rerun()
        with col3:
            # Create clickable status buttons
            status_options = ["Not started", "In progress", "Done"]
            current_status = task['status']
            
            # Find current status index
            try:
                current_index = status_options.index(current_status)
            except ValueError:
                current_index = 0
            
            # Create selectbox for status change
            new_status = st.selectbox(
                "Status:",
                status_options,
                index=current_index,
                key=f"status_{task['id']}",
                label_visibility="collapsed"
            )
            
            # Check if status changed
            if new_status != current_status:
                with st.spinner("Updating status..."):
                    # Update task status in Notion
                    try:
                        task_manager.update_task_status(task['id'], new_status)
                        st.success(f"✅ Status updated to {new_status}")
                        st.toast(f"🎉 Status changed to {new_status}!", icon="✅")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to update status: {e}")
                        st.toast("❌ Failed to update status", icon="⚠️")
        with col4:
            # Status icon using StyleHelper
            style_helper.create_status_icon(task['status'])
        with col5:
            if st.button("Delete", type="primary", key=f"delete_{task['id']}", help="Delete task"):
                with st.spinner("Deleting task..."):
                    result = task_manager.delete_task(task['id'])
                    if result:
                        st.success(f"✅ Task '{task['name']}' deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete task. Please try again.")
        st.markdown("---")
        
        # Handle editing mode for this specific task - show right below the row
        if st.session_state.get(f"editing_{task['id']}", False):
            col1, col2 = st.columns([5, 1])
            with col1:
                new_name = st.text_input(
                    "Task Name:",
                    value=task['name'],
                    key=f"edit_name_{task['id']}",
                    label_visibility="visible"
                )
            with col2:
                # Buttons container with much closer spacing
                st.markdown('<div style="padding-top: 1.75rem;">', unsafe_allow_html=True)
                button_col1, button_col2 = st.columns([1, 1], gap="small")
                with button_col1:
                    if st.button("Save", key=f"save_{task['id']}", type="primary"):
                        if new_name.strip() and new_name != task['name']:
                            with st.spinner("Updating name..."):
                                try:
                                    task_manager.update_task_name(task['id'], new_name.strip())
                                    st.success(f"✅ Name updated to '{new_name.strip()}'")
                                    st.toast(f"🎉 Task name updated!", icon="✅")
                                    st.session_state[f"editing_{task['id']}"] = False
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Failed to update name: {e}")
                                    st.toast("❌ Failed to update name", icon="⚠️")
                        else:
                            st.warning("Please enter a different name")
                with button_col2:
                    if st.button("Cancel", key=f"cancel_{task['id']}"):
                        st.session_state[f"editing_{task['id']}"] = False
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")
    
    
    # Show summary
    if status_filter == "All":
        # Calculate counts
        in_progress_count = len([task for task in tasks if task['status'] == 'In progress'])
        not_started_count = len([task for task in tasks if task['status'] == 'Not started'])
        done_count = len([task for task in tasks if task['status'] == 'Done'])
        
        # Create bordered metrics using StyleHelper
        style_helper.create_bordered_metrics(
            total_tasks=len(tasks),
            in_progress=in_progress_count,
            not_started=not_started_count,
            done=done_count
        )
    else:
        st.metric(f"Filtered Tasks ({status_filter})", len(tasks))
        
else:
    st.error("No tasks found or error loading tasks")

# Refresh button
if st.button("🔄 Refresh Tasks", type="secondary"):
    st.rerun()
