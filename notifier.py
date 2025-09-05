from plyer import notification

def send_nudge_notification(window_title):
    try:
        notification.notify(
            title="GET BACK TO WORK",
            message=f"You are watching: {window_title}",
            app_name="Productivity Tracker",
            timeout=10
        )
        print(f"Notification sent for window: {window_title}")
    except Exception as e:
        print(f"Error sending) notification: {e}")