"""
Notion Database Manager Module

This module provides a task management interface for Notion databases.
It handles all communication with the Notion API for CRUD operations on tasks.

Classes:
    NotionTaskManager: Main class for managing tasks in a Notion database

Functions:
    - list_tasks: Retrieve tasks with optional status filtering
    - add_task: Create new tasks
    - delete_task: Archive tasks
    - restore_task: Unarchive tasks
    - update_task_status: Modify task status
    - update_task_name: Modify task name
"""

from notion_client import Client
import streamlit as st
from task_manager_interface import TaskManagerInterface

class NotionTaskManager(TaskManagerInterface):
    """
    A manager class for interacting with Notion database to perform task operations.
    
    This class provides methods to create, read, update, and delete tasks in a Notion
    database. It uses the official Notion API client to communicate with Notion.
    
    Implemented as a Singleton to ensure only one instance exists throughout the application.
    
    Attributes:
        notion (Client): The Notion API client instance
        database_id (str): The ID of the Notion database to manage
    """
    
    _instance = None
    
    def __new__(cls):
        """Control instance creation to ensure singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        """Get the singleton NotionTaskManager instance"""
        return NotionTaskManager()
    
    def __init__(self):
        """Initialize the NotionTaskManager. Only runs once for the singleton instance."""
        # Only initialize once
        if not hasattr(self, 'notion'):
            auth_token = st.secrets["NOTION_AUTH_TOKEN"]
            database_id = st.secrets["NOTION_DATABASE_ID"]
            self.notion = Client(auth=auth_token)
            self.database_id = database_id
    
    def list_tasks(self, status_filter=None):
        """List all tasks, optionally filtered by status"""
        try:
            print(f"Debug: Querying database {self.database_id} with filter: {status_filter}")
            
            if status_filter:
                response = self.notion.databases.query(
                    database_id=self.database_id,
                    filter={
                        "property": "Status",
                        "status": {
                            "equals": status_filter
                        }
                    }
                )
            else:
                response = self.notion.databases.query(database_id=self.database_id)
            
            print(f"Debug: API returned {len(response['results'])} pages")
            
            tasks = []
            for page in response['results']:
                print(f"Debug: Processing page {page['id']}")
                task = {
                    'id': page['id'],
                    'name': page['properties']['Name']['title'][0]['text']['content'],
                    'status': page['properties']['Status']['status']['name']
                }
                tasks.append(task)
            
            print(f"Debug: Returning {len(tasks)} tasks")
            return tasks
        except Exception as e:
            print(f"Error listing tasks: {e}")
            return []
    
    def add_task(self, name, status="Not Started"):
        """Add a new task to the database"""
        try:
            response = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": name
                                }
                            }
                        ]
                    },
                    "Status": {
                        "status": {
                            "name": status
                        }
                    }
                }
            )
            print(f"Task '{name}' created successfully with ID: {response['id']}")
            return response
        except Exception as e:
            print(f"Error adding task: {e}")
            return None
    
    def delete_task(self, task_id):
        """Delete (archive) a task by ID"""
        try:
            response = self.notion.pages.update(
                page_id=task_id,
                archived=True
            )
            print(f"Task {task_id} deleted successfully")
            return response
        except Exception as e:
            print(f"Error deleting task: {e}")
            return None
    
    def restore_task(self, task_id):
        """Restore (unarchive) a task by ID"""
        try:
            response = self.notion.pages.update(
                page_id=task_id,
                archived=False
            )
            print(f"Task {task_id} restored successfully")
            return response
        except Exception as e:
            print(f"Error restoring task: {e}")
            return None
    
    def update_task_status(self, task_id, new_status):
        """Update task status by ID"""
        try:
            response = self.notion.pages.update(
                page_id=task_id,
                properties={
                    "Status": {
                        "status": {
                            "name": new_status
                        }
                    }
                }
            )
            print(f"Task {task_id} status updated to {new_status}")
            return response
        except Exception as e:
            print(f"Error updating task status: {e}")
            return None
    
    def update_task_name(self, task_id, new_name):
        """Update task name by ID"""
        try:
            response = self.notion.pages.update(
                page_id=task_id,
                properties={
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": new_name
                                }
                            }
                        ]
                    }
                }
            )
            print(f"Task {task_id} name updated to {new_name}")
            return response
        except Exception as e:
            print(f"Error updating task name: {e}")
            return None
    
    def clear_all_tasks(self):
        """Archive all tasks from the Notion database"""
        try:
            # Get all tasks
            tasks = self.list_tasks()
            
            if not tasks:
                print("No tasks to clear")
                return True
            
            # Archive each task
            archived_count = 0
            for task in tasks:
                result = self.delete_task(task['id'])
                if result:
                    archived_count += 1
            
            print(f"All tasks cleared from Notion database ({archived_count} tasks archived)")
            return True
        except Exception as e:
            print(f"Error clearing tasks: {e}")
            return False