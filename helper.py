import json
import os

# --- Configuration and Constants ---
CONFIG_FILE = 'config.json'
LOG_FILE = './data/app_data.json' 
USER_DATA_FILE = "./data/user_data.json"

def classify_window(window_title):
    """Classifies the window title as 'productive' or 'unproductive' based on config."""
    # print(f"DEBUG: classify_window called with: '{window_title}'")
    
    try:
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
        # print(f"DEBUG: Config loaded: {type(config)}")
        # print(f"DEBUG: Config keys: {config.keys() if isinstance(config, dict) else 'Not a dict!'}")
        
        productive_keywords = config.get("productive_keywords", [])
        unproductive_keywords = config.get("unproductive_keywords", [])
        
        # print(f"DEBUG: productive_keywords type: {type(productive_keywords)}, value: {productive_keywords}")
        # print(f"DEBUG: unproductive_keywords type: {type(unproductive_keywords)}, value: {unproductive_keywords}")
        
    except Exception as e:
        # print(f"Error in classify_window: {e}")
        return 'neutral'
    
    title_lower = window_title.lower()
    
    for keyword in productive_keywords:
        if keyword.lower() in title_lower:
            return 'productive'
    
    for keyword in unproductive_keywords:
        if keyword.lower() in title_lower:
            return 'unproductive'
    
    return 'neutral'

def load_config():
    """Loads the configuration from config.json."""
    # print("DEBUG: load_config called")
    
    try:
        # Check if user data file exists
        if not os.path.exists(USER_DATA_FILE):
            print(f"DEBUG: {USER_DATA_FILE} does not exist")
            user_data = {}
        else:
            # print(f"DEBUG: Loading {USER_DATA_FILE}")
            with open(USER_DATA_FILE, 'r', encoding='utf-8-sig') as file:
                user_data = json.load(file)
            # print(f"DEBUG: user_data type: {type(user_data)}, content: {user_data}")
        
        # Check if config file exists
        if not os.path.exists(CONFIG_FILE):
            # print(f"DEBUG: {CONFIG_FILE} does not exist, creating default")
            # Create a default config file if it doesn't exist
            default_config = {
                "productive_keywords": ["code", "visual studio", "pycharm", "terminal", "document", "excel", "photoshop"],
                "unproductive_keywords": ["youtube", "facebook", "instagram", "twitter", "tiktok", "netflix"],
                "start_focus_session_in": 5,
                "nudge_cooldown": 5,
                "max_unproductive_session_time": 10
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            # print(f"A default '{CONFIG_FILE}' has been created. Please customize it.")
            return default_config
        
        # print(f"DEBUG: Loading {CONFIG_FILE}")
        with open(CONFIG_FILE, 'r', encoding='utf-8-sig') as file:
            config_file = json.load(file)
        
        # print(f"DEBUG: config_file type: {type(config_file)}, content: {config_file}")
        
        # Validate that config_file is a dictionary
        if not isinstance(config_file, dict):
            # print(f"ERROR: Config file is not a dictionary! It's a {type(config_file)}")
            # print(f"Config file content: {config_file}")
            raise ValueError("Config file must contain a JSON object, not an array")
        
        # Fix: Ensure we get lists, not strings, and handle missing keys
        user_productive = user_data.get("productive_keywords", [])
        user_unproductive = user_data.get("unproductive_keywords", [])
        
        # print(f"DEBUG: user_productive: {user_productive}, type: {type(user_productive)}")
        # print(f"DEBUG: user_unproductive: {user_unproductive}, type: {type(user_unproductive)}")
        
        # Ensure the config has the required keys with default empty lists
        if "productive_keywords" not in config_file:
            config_file["productive_keywords"] = []
        if "unproductive_keywords" not in config_file:
            config_file["unproductive_keywords"] = []
        
        # print(f"Before extending - productive_keywords: {config_file['productive_keywords']}")
        # print(f"Before extending - unproductive_keywords: {config_file['unproductive_keywords']}")
        
        # Only extend if we have valid lists
        if isinstance(user_productive, list):
            config_file["productive_keywords"].extend(user_productive)
        if isinstance(user_unproductive, list):
            config_file["unproductive_keywords"].extend(user_unproductive)
        
        # print(f"DEBUG: After extending - config_file: {config_file}")
        
        # Save the updated config
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_file, f, indent=4)
            
        return config_file
        
    except FileNotFoundError as e:
        print(f"DEBUG: FileNotFoundError: {e}")
        return None
    except json.JSONDecodeError as e:
        # print(f"DEBUG: JSONDecodeError: {e}")
        # print(f"Error: Could not decode JSON. Please check file format.")
        return None
    except Exception as e:
        # print(f"DEBUG: Unexpected error in load_config: {e}")
        # print(f"DEBUG: Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return None

def initialize_log_file():
    """Creates the JSON log file with an empty list if it doesn't exist."""
    # print("DEBUG: initialize_log_file called")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Initialize with empty structure
    initial_data = {"apps": []}
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f)
    print(f"DEBUG: Initialized {LOG_FILE} with empty structure")

def log_activity(start_time, end_time, app_name, window_title=None):
    # print(f"DEBUG: log_activity called - app: {app_name}, title: {window_title}")
    
    duration = (end_time - start_time).total_seconds()
    if duration < 1 or not app_name:
        # print("DEBUG: Skipping log - duration < 1 or no app_name")
        return

    duration = round(duration, 2)
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    # Ensure the folder exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # Load existing logs or create new structure
    if not os.path.exists(LOG_FILE):
        print("DEBUG: Log file doesn't exist, creating new")
        logs = {"apps": []}
    else:
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            print(f"DEBUG: Loaded logs type: {type(logs)}, content preview: {str(logs)[:200]}")
        except json.JSONDecodeError:
            print("DEBUG: JSON decode error, creating new logs")
            logs = {"apps": []}

    if "apps" not in logs:
        logs["apps"] = []
        print("DEBUG: Added apps key to logs")

    # Use window title if available, else app_name
    entry_name = window_title if window_title else app_name

    # Check if entry already exists
    try:
        app_entry = next((item for item in logs["apps"] if item["app_name"] == entry_name), None)
        print(f"DEBUG: Found existing entry: {app_entry is not None}")
    except Exception as e:
        print(f"DEBUG: Error finding existing entry: {e}")
        app_entry = None

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
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)
        print("Successfully saved logs")
    except Exception as e:
        print(f"Error saving logs: {e}")