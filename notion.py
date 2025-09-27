from notion_client import Client

class NotionTaskManager:
    def __init__(self, auth_token, database_id):
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

# Example usage
# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv
    
#     # Load environment variables
#     load_dotenv()
    
#     # Configuration
#     AUTH_TOKEN = os.getenv("NOTION_AUTH_TOKEN")
#     DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    
#     # Initialize task manager
#     task_manager = NotionTaskManager(AUTH_TOKEN, DATABASE_ID)
    
#     # List all tasks
#     print("=== All Tasks ===")
#     all_tasks = task_manager.list_tasks()
#     for task in all_tasks:
#         print(f"ID: {task['id']}, Name: {task['name']}, Status: {task['status']}")
    
    # # List only "In Progress" tasks
    # print("\n=== In Progress Tasks ===")
    # in_progress_tasks = task_manager.list_tasks("In Progress")
    # for task in in_progress_tasks:
    #     print(f"ID: {task['id']}, Name: {task['name']}, Status: {task['status']}")
    
    # # Add a new task
    # print("\n=== Adding New Task ===")
    # new_task = task_manager.add_task("New Task from Python", "Not Started")
    
    # Example of deleting a task (uncomment and provide valid task ID)
    # print("\n=== Deleting Task ===")
    # task_manager.delete_task("your-task-id-here")