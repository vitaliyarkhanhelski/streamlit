import streamlit as st
import pandas as pd
import os
# from dotenv import load_dotenv
from notion import NotionTaskManager
import time

# Load environment variables
# load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Notion Task Manager",
    page_icon="📋",
    layout="wide"
)

# Custom CSS for Edit button, Save button, and page background
st.markdown("""
<style>
    /* Page background - lighter gradient */
    .stApp {
        background: linear-gradient(135deg, #a8b5ff 0%, #b19cd9 100%) !important;
        min-height: 100vh;
    }
    
    /* Main content area background */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        margin: 1rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Header styling */
    .main .block-container h1 {
        color: #1a1a1a !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Subheader styling */
    .main .block-container h2, .main .block-container h3 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* All text content styling - more comprehensive targeting */
    .main .block-container p,
    .main .block-container div,
    .main .block-container span,
    .main .block-container label,
    .main .block-container .stText,
    .main .block-container .stMarkdown,
    .main .block-container .stWrite,
    .main .block-container .stSelectbox,
    .main .block-container .stTextInput,
    .main .block-container .stDataFrame,
    .main .block-container .stColumns,
    .main .block-container .stMetric,
    .main .block-container .stSuccess,
    .main .block-container .stError,
    .main .block-container .stWarning,
    .main .block-container .stInfo {
        color: #2c3e50 !important;
        font-weight: 500 !important;
    }
    
    /* Strong/bold text */
    .main .block-container strong,
    .main .block-container b {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }
    
    /* Override any Streamlit default text colors */
    .stApp .main .block-container * {
        color: #2c3e50 !important;
    }
    
    /* Specific overrides for Streamlit components */
    .stApp .main .block-container .stText > div,
    .stApp .main .block-container .stMarkdown > div,
    .stApp .main .block-container .stWrite > div {
        color: #2c3e50 !important;
    }
    
    /* Task name text specifically */
    .stApp .main .block-container .stWrite p {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    /* Button styling - white secondary buttons */
    .stButton > button[kind="secondary"] {
        background-color: white !important;
        color: #333333 !important;
        border: 1px solid #cccccc !important;
        border-radius: 5px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #ff4b4b !important;
        color: white !important;
        border-color: #ff4b4b !important;
        transform: translateY(-1px) scale(1.1) !important;
    }
    
    /* Make all primary buttons green by default */
    .stButton > button[kind="primary"] {
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #218838 !important;
        transform: scale(1.1) !important;
    }
    
    /* Override Add Task button to be red */
    .stForm .stButton > button[kind="primary"] {
        background-color: #ff4b4b !important;
        transition: all 0.3s ease !important;
    }
    .stForm .stButton > button[kind="primary"]:hover {
        background-color: #ff3333 !important;
        transform: scale(1.1) !important;
    }
    
    /* Override Refresh button to be blue like Edit button */
    .stButton > button[kind="primary"][data-testid*="refresh"],
    .stButton > button[kind="primary"][aria-label*="Refresh"],
    .stButton > button[kind="primary"]:has-text("Refresh") {
        background-color: #1f77b4 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"][data-testid*="refresh"]:hover,
    .stButton > button[kind="primary"][aria-label*="Refresh"]:hover,
    .stButton > button[kind="primary"]:has-text("Refresh"):hover {
        background-color: #0d5a8a !important;
        transform: translateY(-1px) scale(1.1) !important;
    }
    
    
    /* Universal button hover scaling - more specific selectors */
    .stApp .stButton > button:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Override any conflicting transforms - more specific for Edit button */
    .stApp .stButton > button[kind="secondary"]:hover,
    .stApp .main .block-container .stButton > button[kind="secondary"]:hover,
    .stApp .stButton button[kind="secondary"]:hover {
        transform: translateY(-1px) scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stApp .stButton > button[kind="primary"]:hover {
        transform: scale(1.1) !important;
    }
    
    .stApp .stForm .stButton > button[kind="primary"]:hover {
        transform: scale(1.1) !important;
    }
    
    /* Extra specific rules for Edit button scaling */
    .stApp .stButton button:contains("Edit"):hover,
    .stApp .stButton button[aria-label*="Edit"]:hover {
        transform: translateY(-1px) scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Force scaling on all secondary buttons with !important */
    .stApp .stButton > button[kind="secondary"]:hover {
        transform: translateY(-1px) scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Nuclear option - target all buttons with maximum specificity */
    .stApp .main .block-container .stButton button[kind="secondary"]:hover {
        transform: translateY(-1px) scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Even more specific for the task rows */
    .stApp .main .block-container .stColumns .stButton button[kind="secondary"]:hover {
        transform: translateY(-1px) scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Delete button scaling - multiple specific selectors */
    .stApp .stButton button:contains("Delete"):hover,
    .stApp .stButton button[aria-label*="Delete"]:hover,
    .stApp .main .block-container .stButton button[kind="primary"]:contains("Delete"):hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Force scaling on all primary buttons in task rows */
    .stApp .main .block-container .stColumns .stButton button[kind="primary"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Nuclear option for Delete button - maximum specificity */
    .stApp .main .block-container .stColumns .stButton button[kind="primary"]:hover,
    .stApp .main .block-container .stColumns .stButton button:contains("Delete"):hover,
    .stApp .main .block-container .stColumns .stButton button[aria-label*="Delete"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Override any conflicting transforms for primary buttons */
    .stApp .stButton > button[kind="primary"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Ultra-specific Delete button targeting */
    .stApp .stButton button[data-testid*="delete"]:hover,
    .stApp .stButton button[key*="delete"]:hover,
    .stApp .stButton button[help*="Delete"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Force all primary buttons to scale on hover */
    .stApp .main .block-container .stColumns .stButton button[kind="primary"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Last resort - target primary buttons only */
    .stApp .stButton button[kind="primary"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* JavaScript-based scaling as backup */
    .stApp .stButton button[kind="primary"] {
        transition: all 0.3s ease !important;
    }
    
    /* Form button scaling - Add Task button */
    .stApp .stForm .stButton button[kind="primary"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Force all form buttons to scale */
    .stApp .stForm .stButton button:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Extra specific targeting for Add Task button */
    .stApp .stForm .stButton > button[kind="primary"]:hover,
    .stApp .stForm .stButton button:contains("Add Task"):hover,
    .stApp .stForm .stButton button[aria-label*="Add Task"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Nuclear option for Add Task button */
    .stApp .main .block-container .stForm .stButton button:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Force ALL buttons to scale on hover - ultimate fallback */
    .stApp button:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Override any conflicting styles */
    .stApp .stForm button:hover,
    .stApp .stButton button:hover,
    .stApp button[kind="primary"]:hover,
    .stApp button[kind="secondary"]:hover {
        transform: scale(1.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Push buttons lower with padding */
    .stColumns[data-testid="column"] > div:has(.stButton) {
        padding-top: 1rem !important;
    }
    
    /* Metric cards styling */
    .metric-container {
        background: linear-gradient(45deg, #f8f9fa, #e9ecef) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border-left: 4px solid #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# Add JavaScript to force button scaling
st.markdown("""
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
""", unsafe_allow_html=True)

# Configuration from environment variables
# AUTH_TOKEN = os.getenv("NOTION_AUTH_TOKEN") or st.secrets["NOTION_AUTH_TOKEN"]
AUTH_TOKEN = st.secrets["NOTION_AUTH_TOKEN"]
# DATABASE_ID = os.getenv("NOTION_DATABASE_ID") or st.secrets["NOTION_DATABASE_ID"]
DATABASE_ID = st.secrets["NOTION_DATABASE_ID"]
print(AUTH_TOKEN)
print(DATABASE_ID)

# Initialize task manager
@st.cache_resource
def get_task_manager():
    return NotionTaskManager(AUTH_TOKEN, DATABASE_ID)

# Main app
st.title("📋 Notion Task Manager")
st.markdown("---")

# Initialize task manager
task_manager = get_task_manager()

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



st.markdown("---")

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
            # Green checkmark for Done status
            if task['status'] == "Done":
                st.markdown('<div style="text-align: center; font-size: 1.5rem; color: #28a745;">✅</div>', unsafe_allow_html=True)
            elif task['status'] == "In progress":
                st.markdown('<div style="text-align: center; font-size: 1.5rem; color: #007bff;">⏳</div>', unsafe_allow_html=True)
            else:  # Not started
                st.markdown('<div style="text-align: center; font-size: 1.5rem; color: #6c757d;">⭕</div>', unsafe_allow_html=True)
        with col5:
            if st.button("Delete", type="primary", key=f"delete_{task['id']}", help="Delete task"):
                with st.spinner("Deleting task..."):
                    result = task_manager.delete_task(task['id'])
                    if result:
                        st.success(f"✅ Task '{task['name']}' deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete task. Please try again.")
        
        # Handle editing mode for this specific task - show right below the row
        if st.session_state.get(f"editing_{task['id']}", False):
            st.markdown("---")
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
    
    st.markdown("---")
    
    # Show summary
    if status_filter == "All":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", len(tasks))
        with col2:
            in_progress_count = len([task for task in tasks if task['status'] == 'In progress'])
            st.metric("In Progress", in_progress_count)
        with col3:
            not_started_count = len([task for task in tasks if task['status'] == 'Not started'])
            st.metric("Not Started", not_started_count)
        with col4:
            done_count = len([task for task in tasks if task['status'] == 'Done'])
            st.metric("Done", done_count)
    else:
        st.metric(f"Filtered Tasks ({status_filter})", len(tasks))
        
else:
    st.error("No tasks found or error loading tasks")

# Refresh button
if st.button("🔄 Refresh Tasks", type="secondary"):
    st.rerun()
