import streamlit as st
import os
from dotenv import load_dotenv
from notion_client import Client
load_dotenv()

# def clear_task_name():
#     st.session_state.task_name = ""  # resets the input

task_name = st.text_input(
    "Task Name:",
    placeholder="Enter task name...",
    key="task_name"
)

# Button that clears via callback
# st.button("Clear", on_click=clear_task_name)
st.button("Cleaar")




# Use environment variables for sensitive data
auth_token = os.getenv("NOTION_AUTH_TOKEN")
database_id = os.getenv("NOTION_DATABASE_ID")

print(auth_token)
print(database_id)

if not auth_token or not database_id:
    st.error("❌ Missing environment variables. Please set NOTION_AUTH_TOKEN and NOTION_DATABASE_ID in your .env file")
    st.stop()

try:
    notion = Client(auth=auth_token)
    results = notion.databases.query(database_id=database_id)
    
    st.write("## Tasks from Notion Database")
    for page in results["results"]:
        props = page["properties"]

        # Name (assuming it's a Title property)
        name = props["Name"]["title"][0]["text"]["content"] if props["Name"]["title"] else ""

        # Status (could be Select or Status type)
        if props["Status"]["type"] == "status":
            status = props["Status"]["status"]["name"] if props["Status"]["status"] else ""
        elif props["Status"]["type"] == "select":
            status = props["Status"]["select"]["name"] if props["Status"]["select"] else ""
        else:
            status = ""

        st.write(f"**{name}** - {status}")
        
except Exception as e:
    st.error(f"❌ Error connecting to Notion: {str(e)}")
    st.info("Please check your API token and database ID in the .env file")