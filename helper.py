import json
import os

# --- Configuration and Constants ---
CONFIG_FILE = './config.json'
LOG_FILE = './data/app_data.json' 
USER_DATA_FILE = "./data/user_data.json"

def classify_window(window_title):
    """Classifies the window title as 'productive' or 'unproductive' based on config."""
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)
    productive_keywords = config.get("productive_keywords", [])
    # unproductive_keywords = config.get("unproductive_keywords", [])
    
    title_lower = window_title.lower()
    if title_lower.strip() == "":
        return 'neutral'

    for keyword in productive_keywords:
        if keyword.lower() in title_lower:
            return 'productive'
    
    # for keyword in unproductive_keywords:
    #     if keyword.lower() in title_lower:
    #         return 'unproductive'
    
    return 'unproductive'

def load_config():
    """Loads the configuration from config.json."""
    try:
        # Check if user data file exists
        if not os.path.exists(USER_DATA_FILE):
            os.mkdir(os.path.dirname(USER_DATA_FILE))
            with open(USER_DATA_FILE, 'w') as f:
                json.dump({}, f)
        else:
            with open(USER_DATA_FILE, 'r', encoding='utf-8-sig') as file:
                user_data = json.load(file)
        
        # Check if config file exists
        if not os.path.exists(CONFIG_FILE):
            # Create a default config file if it doesn't exist
            default_config = {
                "productive_keywords": ["code", "visual studio", "pycharm", "terminal", "document", "excel", "photoshop"],
                "unproductive_keywords": ["youtube", "facebook", "instagram", "twitter", "tiktok", "netflix"],
                "start_focus_session_in": 20,
                "nudge_cooldown": 20,
                "max_unproductive_session_time": 10
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            print(f"A default '{CONFIG_FILE}' has been created. Please customize it.")
            return default_config
        
        with open(CONFIG_FILE, 'r', encoding='utf-8-sig') as file:
            config_file = json.load(file)
        
        # Validate that config_file is a dictionary
        if not isinstance(config_file, dict):
            raise ValueError("Config file must contain a JSON object, not an array")
        
        # Get user keywords
        user_productive = user_data.get("productive_keywords", [])
        user_unproductive = user_data.get("unproductive_keywords", [])
        
        # Ensure the config has the required keys with default empty lists
        if "productive_keywords" not in config_file:
            config_file["productive_keywords"] = []
        if "unproductive_keywords" not in config_file:
            config_file["unproductive_keywords"] = []
        
        # Combine all keywords first
        all_productive = config_file["productive_keywords"].copy()
        all_unproductive = config_file["unproductive_keywords"].copy()
        
        # Add user keywords
        if isinstance(user_productive, list):
            all_productive.extend(user_productive)
        if isinstance(user_unproductive, list):
            all_unproductive.extend(user_unproductive)
        
        # Remove duplicates using case-insensitive comparison while preserving original case
        def remove_duplicates_case_insensitive(keyword_list):
            seen_lower = set()
            unique_keywords = []
            for keyword in keyword_list:
                keyword_lower = keyword.lower()
                if keyword_lower not in seen_lower:
                    seen_lower.add(keyword_lower)
                    unique_keywords.append(keyword)
            return unique_keywords
        
        # Apply deduplication
        config_file["productive_keywords"] = remove_duplicates_case_insensitive(all_productive)
        config_file["unproductive_keywords"] = remove_duplicates_case_insensitive(all_unproductive)
        
        print(f"Loaded {len(config_file['productive_keywords'])} productive keywords")
        print(f"Loaded {len(config_file['unproductive_keywords'])} unproductive keywords")
        
        # Save the updated config
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_file, f, indent=4)
            
        return config_file
        
    except FileNotFoundError:
        print(f"Error: File not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON. Please check file format.")
        return None
    except Exception as e:
        print(f"Unexpected error in load_config: {e}")
        return None
        
    except FileNotFoundError:
        print(f"Error: File not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON. Please check file format.")
        return None
    except Exception as e:
        print(f"Unexpected error in load_config: {e}")
        return None

def initialize_log_file():
    """Creates the JSON log file with proper structure."""
    # Create directory if it doesn't exist
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE))
    
    # Initialize with proper structure
    initial_data = {"apps": []}
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f)

def log_activity(start_time, end_time, app_name, window_title=None):
    """Log activity to the JSON file."""
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
            if not isinstance(logs, dict) or "apps" not in logs:
                logs = {"apps": []}
        except json.JSONDecodeError:
            logs = {"apps": []}

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