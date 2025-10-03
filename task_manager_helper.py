"""
Task Manager Helper Module

This module provides helper functions for the task manager application.

Classes:
    TaskManagerHelper: Helper class for task management operations
"""

import streamlit as st
import time
from task_manager_interface import TaskManagerInterface
from notion_manager import NotionTaskManager
from sql_manager import SqlTaskManager


class TaskManagerHelper:
    """Helper class for task management operations"""
    
    @staticmethod
    @st.cache_resource
    def get_task_manager(backend: str) -> TaskManagerInterface:
        """
        Get the appropriate task manager based on the selected backend.
        
        Args:
            backend (str): Either "Notion" or "SQLite"
        
        Returns:
            TaskManagerInterface: An instance implementing the TaskManagerInterface
        """
        if backend == "Notion":
            try:
                return NotionTaskManager.get_instance()
            except Exception as e:
                st.error(f"❌ Notion configuration error: {e}")
                st.info("💡 Falling back to SQLite. Please configure Notion secrets to use Notion backend.")
                return SqlTaskManager.get_instance()
        else:
            return SqlTaskManager.get_instance()
    
    @staticmethod
    def show_sync_confirmation_dialog():
        """
        Display sync confirmation dialog and handle the sync operation.
        
        This method shows a confirmation dialog when user wants to copy tasks
        from Notion to SQLite, and executes the sync if confirmed.
        """
        # Initial sync button
        if st.button("📥 Copy From Notion to SQLite", type="primary", use_container_width=True):
            st.session_state.show_sync_confirmation = True

        # Show confirmation dialog if button was clicked
        if st.session_state.get('show_sync_confirmation', False):
            st.warning("⚠️ This will replace all tasks in SQLite with tasks from Notion. Are you sure?")
            
            if st.button("✅ Yes, Sync Now", type="primary", use_container_width=True):
                st.session_state.show_sync_confirmation = False
                TaskManagerHelper._execute_sync()
        
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_sync_confirmation = False
                st.rerun()
    
    @staticmethod
    def _execute_sync():
        """
        Execute the sync operation from Notion to SQLite.
        
        This internal method handles the actual syncing process:
        - Fetches all tasks from Notion
        - Clears SQLite database
        - Copies tasks to SQLite
        """
        with st.spinner("Syncing data from Notion to SQLite..."):
            time.sleep(1)
            try:
                # Initialize both managers
                notion_manager = NotionTaskManager.get_instance()
                sqlite_manager = SqlTaskManager.get_instance()
                
                # Fetch all tasks from Notion
                notion_tasks = notion_manager.list_tasks()
                
                if notion_tasks:
                    # Clear all tasks from SQLite
                    sqlite_manager.clear_all_tasks()
                    
                    # Add all tasks from Notion to SQLite
                    success_count = 0
                    for task in notion_tasks:
                        result = sqlite_manager.add_task(task['name'], task['status'])
                        if result:
                            success_count += 1
                    
                    st.success(f"✅ Successfully synced {success_count} tasks from Notion to SQLite!")
                    st.toast(f"🎉 Synced {success_count} tasks!", icon="✅")
                    # Small delay to let the toast display before switching
                    time.sleep(1.5)
                    # Switch to SQLite backend to view synced data
                    st.session_state.selected_backend = "SQLite"
                    st.rerun()
                else:
                    st.warning("⚠️ No tasks found in Notion database")
                    
            except KeyError:
                st.error("❌ Notion credentials not found. Please configure .streamlit/secrets.toml")
            except Exception as e:
                st.error(f"❌ Error syncing data: {e}")
                st.toast("❌ Sync failed", icon="⚠️")

