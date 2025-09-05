import json
import os

# --- Configuration and Constants ---
CONFIG_FILE = 'config.json'
LOG_FILE = './data/app_data.json' 

def classify_window(window_title):
    """Classifies the window title as 'productive' or 'unproductive' based on config."""
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)
    productive_keywords = config.get("productive_keywords", [])
    unproductive_keywords = config.get("unproductive_keywords", [])
    
    title_lower = window_title.lower()
    
    for keyword in unproductive_keywords:
        if keyword.lower() in title_lower:
            return 'unproductive'
        
    for keyword in productive_keywords:
        if keyword.lower() in title_lower:
            return 'productive'
    
    
    return 'neutral'

def load_config():
    """Loads the configuration from config.json."""
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: '{CONFIG_FILE}' not found. Please create it.")
        # Create a default config file if it doesn't exist
        default_config = {
            "productive_apps": ["code", "visual studio", "pycharm", "terminal", "document", "excel", "photoshop"],
            "start_focus_session_in": 5,
            "nudge_cooldown": 5
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f"A default '{CONFIG_FILE}' has been created. Please customize it.")
        return default_config
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{CONFIG_FILE}'. Please check its format.")
        return None

def initialize_log_file():
    """Creates the JSON log file with an empty list if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

# Reads, updates, and writes the aggregated activity log to the JSON file.
# helper.py
def log_activity(start_time, end_time, app_name, window_title=None):
    duration = (end_time - start_time).total_seconds()
    if duration < 1 or not app_name:
        return

    duration = round(duration, 2)
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    # Ensure the folder exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Load existing logs or create new structure
    if not os.path.exists(LOG_FILE):
        logs = {"apps": []}
    else:
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = {"apps": []}

    if "apps" not in logs:
        logs["apps"] = []

    # Use window title if available, else app_name
    entry_name = window_title if window_title else app_name

    # Check if entry already exists
    app_entry = next((item for item in logs["apps"] if item["app_name"] == entry_name), None)

    if app_entry:
        app_entry["total_time_spent"] += duration
        if duration > app_entry["longest_session"]:
            app_entry["longest_session"] = duration
        app_entry["last_active"] = end_time_str
    else:
        new_entry = {
            "app_name": entry_name,
            "total_time_spent": duration,
            "longest_session": duration,
            "last_active": end_time_str
        }
        logs["apps"].append(new_entry)

    # Save back to file
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2)
