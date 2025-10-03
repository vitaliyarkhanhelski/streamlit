"""
SQLite Database Manager Module

This module provides a task management interface for SQLite databases.
It handles all database operations for CRUD operations on tasks using SQLite.

Classes:
    SqlTaskManager: Main class for managing tasks in a SQLite database

Functions:
    - list_tasks: Retrieve tasks with optional status filtering
    - add_task: Create new tasks
    - delete_task: Mark tasks as archived
    - restore_task: Unarchive tasks
    - update_task_status: Modify task status
    - update_task_name: Modify task name
"""

import sqlite3
import uuid
from datetime import datetime
from task_manager_interface import TaskManagerInterface


class SqlTaskManager(TaskManagerInterface):
    """
    A manager class for interacting with SQLite database to perform task operations.
    
    This class provides methods to create, read, update, and delete tasks in a SQLite
    database. It mirrors the interface of NotionTaskManager for easy switching.
    
    Implemented as a Singleton to ensure only one instance exists throughout the application.
    
    Attributes:
        db_path (str): Path to the SQLite database file
    """
    
    _instance = None
    
    def __new__(cls, db_path="tasks.db"):
        """Control instance creation to ensure singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @staticmethod
    def get_instance(db_path="tasks.db"):
        """Get the singleton SqlTaskManager instance"""
        return SqlTaskManager(db_path)
    
    def __init__(self, db_path="tasks.db"):
        """Initialize the SQLite task manager and create tables if needed. Only runs once for the singleton instance."""
        # Only initialize once
        if not hasattr(self, 'db_path'):
            self.db_path = db_path
            self._init_database()
    
    def _init_database(self):
        """Create the tasks table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                archived INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def list_tasks(self, status_filter=None):
        """List all tasks, optionally filtered by status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if status_filter:
                cursor.execute(
                    'SELECT id, name, status FROM tasks WHERE status = ? AND archived = 0',
                    (status_filter,)
                )
            else:
                cursor.execute('SELECT id, name, status FROM tasks WHERE archived = 0')
            
            rows = cursor.fetchall()
            conn.close()
            
            tasks = []
            for row in rows:
                task = {
                    'id': row[0],
                    'name': row[1],
                    'status': row[2]
                }
                tasks.append(task)
            
            print(f"Debug: SQLite returned {len(tasks)} tasks")
            return tasks
        except Exception as e:
            print(f"Error listing tasks: {e}")
            return []
    
    def add_task(self, name, status="Not started"):
        """Add a new task to the database"""
        try:
            task_id = str(uuid.uuid4())
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO tasks (id, name, status, archived) VALUES (?, ?, ?, 0)',
                (task_id, name, status)
            )
            
            conn.commit()
            conn.close()
            
            print(f"Task '{name}' created successfully with ID: {task_id}")
            return {'id': task_id, 'name': name, 'status': status}
        except Exception as e:
            print(f"Error adding task: {e}")
            return None
    
    def delete_task(self, task_id):
        """Delete (archive) a task by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE tasks SET archived = 1, updated_at = ? WHERE id = ?',
                (datetime.now(), task_id)
            )
            
            conn.commit()
            conn.close()
            
            print(f"Task {task_id} deleted successfully")
            return {'id': task_id, 'archived': True}
        except Exception as e:
            print(f"Error deleting task: {e}")
            return None
    
    def restore_task(self, task_id):
        """Restore (unarchive) a task by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE tasks SET archived = 0, updated_at = ? WHERE id = ?',
                (datetime.now(), task_id)
            )
            
            conn.commit()
            conn.close()
            
            print(f"Task {task_id} restored successfully")
            return {'id': task_id, 'archived': False}
        except Exception as e:
            print(f"Error restoring task: {e}")
            return None
    
    def update_task_status(self, task_id, new_status):
        """Update task status by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?',
                (new_status, datetime.now(), task_id)
            )
            
            conn.commit()
            conn.close()
            
            print(f"Task {task_id} status updated to {new_status}")
            return {'id': task_id, 'status': new_status}
        except Exception as e:
            print(f"Error updating task status: {e}")
            return None
    
    def update_task_name(self, task_id, new_name):
        """Update task name by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE tasks SET name = ?, updated_at = ? WHERE id = ?',
                (new_name, datetime.now(), task_id)
            )
            
            conn.commit()
            conn.close()
            
            print(f"Task {task_id} name updated to {new_name}")
            return {'id': task_id, 'name': new_name}
        except Exception as e:
            print(f"Error updating task name: {e}")
            return None
    
    def clear_all_tasks(self):
        """Delete all tasks from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM tasks')
            
            conn.commit()
            conn.close()
            
            print("All tasks cleared from SQLite database")
            return True
        except Exception as e:
            print(f"Error clearing tasks: {e}")
            return False
    
    def clear_tasks_by_status(self, status):
        """Delete all tasks with a specific status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM tasks WHERE status = ? AND archived = 0', (status,))
            deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            print(f"Cleared {deleted_count} tasks with status '{status}' from SQLite database")
            return True
        except Exception as e:
            print(f"Error clearing tasks by status: {e}")
            return False

