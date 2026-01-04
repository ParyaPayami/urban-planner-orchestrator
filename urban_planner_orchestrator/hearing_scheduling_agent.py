# hearing_scheduling_agent.py
from datetime import datetime, timedelta

class HearingSchedulingAgent:
    """
    Agent responsible for scheduling public hearings and recording their outcomes.
    """
    def __init__(self):
        # Example schedule: hearings happen every first Monday of the month at 10 AM (simplified)
        self.default_hearing_days = [1]  # (Not fully used in dummy logic)

    def schedule_hearing(self, application):
        """
        Schedule a hearing for the application and set a hearing date.
        Returns the scheduled date.
        """
        # For simplicity, schedule 30 days from now at 10:00 AM
        hearing_date = datetime.now() + timedelta(days=30)
        hearing_date = hearing_date.replace(hour=10, minute=0, second=0, microsecond=0)
        application['hearing_date'] = hearing_date
        application['status'] = 'Hearing Scheduled'
        # Decide hearing type based on application (e.g., Planning Commission or Admin Hearing)
        if application.get('requires_hearing'):
            application['hearing_type'] = 'Public Hearing'
        else:
            application['hearing_type'] = 'N/A'
        return hearing_date

    def record_outcome(self, application, decision):
        """
        Record the outcome of the hearing (e.g., approved or denied).
        """
        # Normalize decision string
        decision = decision.strip().lower()
        if 'approve' in decision:
            application['hearing_outcome'] = 'Approved'
            application['status'] = 'Approved'
        elif 'deny' in decision:
            application['hearing_outcome'] = 'Denied'
            application['status'] = 'Denied'
        else:
            application['hearing_outcome'] = decision
            application['status'] = 'Pending Decision'
        return application['hearing_outcome']
