"""
Task Manager Interface Module

This module provides an abstract base class that defines the interface
for all task manager implementations.

Classes:
    TaskManagerInterface: Abstract base class for task managers
"""

from abc import ABC, abstractmethod


class TaskManagerInterface(ABC):
    """
    Abstract base class defining the interface for task management systems.
    
    All task manager implementations (Notion, SQLite, etc.) must inherit from
    this class and implement all abstract methods to ensure consistent behavior.
    """
    
    @abstractmethod
    def list_tasks(self, status_filter=None):
        """
        List all tasks, optionally filtered by status.
        
        Args:
            status_filter (str, optional): Filter tasks by status
        
        Returns:
            list: List of task dictionaries with keys: id, name, status
        """
        pass
    
    @abstractmethod
    def add_task(self, name, status="Not started"):
        """
        Add a new task to the database.
        
        Args:
            name (str): Task name
            status (str): Initial status (default: "Not started")
        
        Returns:
            dict or None: Created task information or None on error
        """
        pass
    
    @abstractmethod
    def delete_task(self, task_id):
        """
        Delete (archive) a task by ID.
        
        Args:
            task_id (str): Unique identifier of the task
        
        Returns:
            dict or None: Response information or None on error
        """
        pass
    
    @abstractmethod
    def restore_task(self, task_id):
        """
        Restore (unarchive) a task by ID.
        
        Args:
            task_id (str): Unique identifier of the task
        
        Returns:
            dict or None: Response information or None on error
        """
        pass
    
    @abstractmethod
    def update_task_status(self, task_id, new_status):
        """
        Update task status by ID.
        
        Args:
            task_id (str): Unique identifier of the task
            new_status (str): New status value
        
        Returns:
            dict or None: Updated task information or None on error
        """
        pass
    
    @abstractmethod
    def update_task_name(self, task_id, new_name):
        """
        Update task name by ID.
        
        Args:
            task_id (str): Unique identifier of the task
            new_name (str): New task name
        
        Returns:
            dict or None: Updated task information or None on error
        """
        pass
    
    @abstractmethod
    def clear_all_tasks(self):
        """
        Clear all tasks from the database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def clear_tasks_by_status(self, status):
        """
        Clear all tasks with a specific status.
        
        Args:
            status (str): Status to filter tasks by (e.g., "Done", "Not started", "In progress")
        
        Returns:
            bool: True if successful, False otherwise
        """
        pass

