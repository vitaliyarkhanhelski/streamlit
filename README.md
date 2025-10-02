# 📋 Notion Task Manager

A beautiful, modern web application for managing tasks in Notion databases. Built with Streamlit, this application provides an intuitive interface for creating, editing, filtering, and managing tasks with real-time synchronization to your Notion workspace.

## ✨ Features

- **➕ Add Tasks**: Create new tasks with customizable status (Not started, In progress, Done)
- **🔍 Filter Tasks**: Filter tasks by status to focus on what matters
- **✏️ Edit Tasks**: Inline editing of task names with instant updates
- **🔄 Update Status**: Change task status using convenient dropdown selectors
- **🗑️ Delete Tasks**: Archive tasks when completed or no longer needed
- **📊 Visual Dashboard**: Metrics dashboard showing task statistics at a glance
- **🎨 Beautiful UI**: Gradient background with glassmorphism effects and modern design
- **⚡ Real-time Sync**: All changes are instantly synchronized with your Notion database
- **🎯 Status Icons**: Visual indicators for task status (✅ Done, ⏳ In Progress, ⭕ Not Started)

## 🚀 Prerequisites

- Python 3.8 or higher
- A Notion account with API access
- A Notion database set up for task management

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### 1. Set up Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration" and give it a name
3. Copy the "Internal Integration Token" (starts with `secret_`)
4. Share your Notion database with the integration:
   - Open your database in Notion
   - Click "..." menu → "Add connections"
   - Select your integration

### 2. Get Database ID

The database ID is the string in your database URL:
```
https://www.notion.so/workspace/DATABASE_ID?v=...
```

### 3. Configure Secrets

Create a `.streamlit/secrets.toml` file in the project directory:

```toml
NOTION_AUTH_TOKEN = "secret_xxxxxxxxxxxxx"
NOTION_DATABASE_ID = "xxxxxxxxxxxxx"
```

**Security Note**: Never commit `secrets.toml` to version control. It's already included in `.gitignore`.

## 🎯 Usage

Run the application:
```bash
streamlit run notion_streamlit.py
```

The app will open in your default browser at `http://localhost:8501`.

### Using the Application

1. **Add a Task**: Fill in the task name and select a status, then click "Add Task"
2. **Filter Tasks**: Use the status filter dropdown to view specific task categories
3. **Edit a Task**: Click the "Edit" button next to a task, modify the name, and click "Save"
4. **Update Status**: Use the status dropdown in each task row to change the task status
5. **Delete a Task**: Click the "Delete" button to remove a task (archives it in Notion)
6. **View Metrics**: See task statistics at the bottom of the page

## 📁 Project Structure

```
streamlit/
├── notion_streamlit.py    # Main Streamlit application
├── notion_manager.py      # Notion API integration layer
├── style_helper.py        # Custom styling utilities
├── styles.css            # CSS styling for the app
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .streamlit/
    └── secrets.toml     # Configuration (not in repo)
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Notion API](https://developers.notion.com/)** - Notion database integration
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation
- **[notion-client](https://github.com/ramnes/notion-sdk-py)** - Python SDK for Notion API
- **Custom CSS** - Beautiful gradient UI with glassmorphism effects

## 🎨 UI Features

- **Gradient Background**: Soft purple/lavender gradient (#c6cffd to #d0c3e8)
- **Glassmorphism**: Semi-transparent containers with backdrop blur
- **Color-coded Buttons**: 
  - Primary actions (Delete, Save): Green (#28a745)
  - Form submissions (Add Task): Red (#ff4b4b)
  - Secondary actions (Edit, Refresh): White with red hover
- **Compact Layout**: Optimized spacing for viewing more tasks
- **Responsive Design**: Works on different screen sizes

## 🔧 Notion Database Schema

Your Notion database should have at least these properties:

| Property | Type | Description |
|----------|------|-------------|
| Name | Title | Task name |
| Status | Select | Task status (Not started, In progress, Done) |

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with ❤️ using Streamlit
- Powered by the Notion API
- UI inspired by modern design principles

---

**Made with Streamlit** 🎈
