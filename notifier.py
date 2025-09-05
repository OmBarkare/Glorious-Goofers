from plyer import notification

def send_nudge_notification(window_title):
    try:
        notification.notify(
            title="GET BACK TO WORK",
            message=f"You are watching: {window_title}",
            app_name="Productivity Tracker",
            timeout=5
        )
        print(f"Notification sent for window: {window_title}")
    except Exception as e:
        print(f"Error sending) notification: {e}")

def send_focus_session_start_notification():
    try:
        notification.notify(
            title="Starting Focus Session",
            message=f"Locking In !!",
            app_name="Productivity Tracker",
            timeout=3
        )
        print(f"Notification sent for focus session start")
    except Exception as e:
        print(f"Error sending) notification: {e}")


def send_focus_session_end_warning():
    try:
        notification.notify(
            title="STAY FOCUSED",
            message=f"You have been productive for a while. Don't break the streak!",
            app_name="Productivity Tracker",
            timeout=3
        )
        print(f"Notification sent for focus session start")
    except Exception as e:
        print(f"Error sending) notification: {e}")

def send_focus_session_end_notification_after_warning():
    try:
        notification.notify(
            title="Focus Session Ended",
            message=f"You Are getting distracted! Time to take a break.",
            app_name="Productivity Tracker",
            timeout=7
        )
        print(f"Notification sent for focus session end")
    except Exception as e:
        print(f"Error sending) notification: {e}")