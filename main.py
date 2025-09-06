import pywinctl as pwc
from analyze import analyze_data
from plyer import notification
import time
from helper import (
    load_config,
    initialize_log_file,
    log_activity,
    classify_window)
from notifier import (send_nudge_notification, send_focus_session_start_notification, send_focus_session_end_warning, send_focus_session_end_notification_after_warning)
import json
import os
from datetime import datetime, timedelta
from display import load_and_display_dashboard

USER_DATA_FILE = "./data/user_data.json"
LOG_FILE = './data/app_data.json'
CHECK_INTERVAL_SECONDS = 0.5
ANALYZE_INTERVAL_SECONDS = 300  # Analyze every 5 minutes

# def send_nudge_notification(distracting_app_title):
#     """Sends a desktop notification to nudge the user back to a productive task."""
#     try:
#         notification.notify(
#             title="Stay Focused!",
#             message=f"You switched to {distracting_app_title}. Want to get back to your focus session?",
#             app_name="Productivity Tracker",
#             timeout=10  # Notification will disappear after 10 seconds
#         )
#         print(f"Sent a nudge notification about '{distracting_app_title}'.")
#     except Exception as e:
#         print(f"Error sending notification: {e}")
#         print("Please ensure you have a notification backend installed (e.g., on Linux, `sudo apt-get install libnotify-bin`).")


# --- Main Application Logic ---

def main():
    """The main loop to track window activity."""
    config = load_config()
    if not config:
        return

    initialize_log_file()

    # State variables
    last_window_title = None
    current_window_title = None
    last_app_name = None
    current_window_category = 'neutral'
    activity_start_time = datetime.now()
    unproductive_session_start = None
    productive_session_end_warning_counter = 0
    unproductive_session_warning_counter = 0
    productive_start_time = None
    in_focus_session = False
    last_nudge_time = 0
    FOCUS_SESSION_THRESHOLD = config.get("start_focus_session_in", 5)
    NUDGE_COOLDOWN_SECONDS = config.get("nudge_cooldown", 5)
    MAX_UNPRODUCTIVE_SESSION_TIME = config.get("max_unproductive_session_time", 10)

    print("Productivity Tracker started. Press Ctrl+C to stop.")

    try:
        while True:
            active_window = pwc.getActiveWindow()
            current_window_title = active_window.title if active_window else ""
            current_app_name = active_window.getAppName() if active_window else ""

            if current_window_title != last_window_title:
                # When the window changes, log the time spent on the previous one
                end_time = datetime.now()
                
                # Log the previous activity
                if last_window_title is not None:
                    log_activity(activity_start_time, end_time, last_app_name, last_window_title)
                    current_window_category = classify_window(current_window_title)
                    print(f"Switched from '{last_window_title}' ()")

                # Reset the timer and title for the new window
                activity_start_time = datetime.now()
                last_window_title = current_window_title
                last_app_name = current_app_name
                
                # current_category = classify_window(current_window_title, config)
                print(f"Current window: '{current_window_title}' ")

                # --- Focus Session Logic ---
                # if (end_time - datetime.now()) >= timedelta(seconds=START_FOCUS_TIME):
                #     in_focus_session = True# Check if enough time has passed since the last nudge
                #     time_since_last_nudge = time.time() - last_nudge_time
                #     if time_since_last_nudge > timedelta(seconds=NUDGE_COOLDOWN_SECONDS):
                #         send_nudge_notification(current_window_title)
                #         last_nudge_time = time.time()
                #     else:
                #         print("In cooldown period. Skipping nudge.")
                # if current_category == 'productive':
                #     if not in_focus_session:
                #         print("Productive app detected. Starting a focus session!")
                #         in_focus_session = True
                
                # elif current_category == 'unproductive':
                    
                    # Switching to an unproductive app ends the focus session
                    # if in_focus_session:
                    #     print("Unproductive app detected. Ending focus session.")
                    #     in_focus_session = False

            if current_window_category == 'productive':
                if productive_start_time is not None:
                    productive_elapsed = (datetime.now() - productive_start_time).total_seconds()
                    if not in_focus_session and productive_elapsed >= FOCUS_SESSION_THRESHOLD:
                        in_focus_session = True
                        send_focus_session_start_notification()
                        print("Focus session started automatically!")
                else:
                    productive_start_time = datetime.now()
                    unproductive_session_start = None
            else:
                if in_focus_session:
                    cooldown = (time.time() - last_nudge_time)
                    if cooldown >= NUDGE_COOLDOWN_SECONDS:
                        if productive_session_end_warning_counter < 3:
                            send_focus_session_end_warning()
                        else:
                            print("Focus session ended due to unproductive activity.")
                            in_focus_session = False
                            productive_start_time = None
                            productive_session_end_warning_counter = 0
                            send_focus_session_end_notification_after_warning()
                            if last_window_title is not None:
                                log_activity(activity_start_time, end_time, last_app_name, last_window_title)

                            end_time = datetime.now()
                            log_activity(activity_start_time, end_time, last_app_name, last_window_title)
                            analyze_data(LOG_FILE)
                            load_and_display_dashboard(USER_DATA_FILE)
                            load_config()
                        productive_session_end_warning_counter += 1
                        last_nudge_time = time.time()

                else:
                    in_focus_session = False
                    productive_start_time = None

            if not in_focus_session and current_window_category == 'unproductive':
                cooldown = (time.time() - last_nudge_time)
                if unproductive_session_start is None:
                    unproductive_session_start = datetime.now()
                else:
                    elapsed = (datetime.now() - unproductive_session_start).total_seconds()
                    if elapsed >= MAX_UNPRODUCTIVE_SESSION_TIME and cooldown >= NUDGE_COOLDOWN_SECONDS:
                        if unproductive_session_warning_counter < 3:
                            send_nudge_notification(current_window_title)
                            last_nudge_time = time.time()
                            unproductive_session_warning_counter += 1
                        else:
                            unproductive_session_start = None
                            unproductive_session_warning_counter = 0
                            # log_activity(activity_start_time, end_time, last_app_name, last_window_title)
            
                            end_time = datetime.now()
                            log_activity(activity_start_time, end_time, last_app_name, last_window_title)
                            analyze_data(LOG_FILE)
                            load_and_display_dashboard(USER_DATA_FILE)
                            load_config()
                        print("You've been unproductive for a while. Time to focus!")
                        unproductive_session_start = None
            print("Current Window Category: ",current_window_category)
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        # Log the final activity before exiting
        end_time = datetime.now()
        # if last_window_title is not None:
        #     log_activity(activity_start_time, end_time, last_app_name, last_window_title)
            
        # analyze_data(LOG_FILE)
        # load_and_display_dashboard(USER_DATA_FILE)
        log_activity(activity_start_time, end_time, last_app_name, last_window_title)
            
        analyze_data(LOG_FILE)
        load_and_display_dashboard(USER_DATA_FILE)
        load_config()
        print("\nTracker stopped. Final activity logged.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
