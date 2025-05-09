# notification_agent.py
class NotificationAgent:
    """
    Agent responsible for sending notifications (emails, alerts) to applicants, staff, and other stakeholders.
    """
    def send_notification(self, recipient, content):
        """
        Send a notification to a single recipient.
        """
        # In a real system, this might send an email or SMS. Here we'll just simulate with a print.
        print(f"[Notification] To: {recipient} -> {content}")
        return True

    def send_notifications(self, recipients, content):
        """
        Send a notification to multiple recipients.
        """
        if isinstance(recipients, list):
            for rec in recipients:
                print(f"[Notification] To: {rec} -> {content}")
        else:
            # if a single recipient is passed as string
            print(f"[Notification] To: {recipients} -> {content}")
        return True
