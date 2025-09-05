import json
import os

# --- Configuration and Constants ---
CONFIG_FILE = 'config.json'
LOG_FILE = './data/app_data.json' 

def load_config():
    """Loads the configuration from config.json."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
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
def log_activity(start_time, end_time, app_name):
    duration = (end_time - start_time).total_seconds()
    
    if duration < 1 or not app_name:
        return

    duration = int(duration)
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    # Find if the app already has an entry
    app_entry = next((item for item in logs if item.get('app_name') == app_name), None)

    if app_entry:
        # Update existing entry
        app_entry['total_time_spent'] += duration
        app_entry['last_active'] = end_time_str
        if duration > app_entry['longest_session']:
            app_entry['longest_session'] = duration
    else:
        # Create new entry
        new_entry = {
            'app_name': app_name,
            'last_active': end_time_str,
            'total_time_spent': duration,
            'longest_session': duration
        }
        logs.append(new_entry)

    # Write the updated data back to the file
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2)

