# application_intake_agent.py
class ApplicationIntakeAgent:
    """
    Agent responsible for receiving and logging new permit applications.
    It assigns application IDs and checks for completeness of submission.
    """
    def __init__(self):
        # Initialize an ID counter for new applications
        self.next_id = 1

    def check_completeness(self, application_data):
        """
        Check if the application data has all required fields.
        Returns True if complete, False if some mandatory info is missing.
        """
        # For simplicity, assume required fields are 'address' and 'applicant_name'
        required_fields = ['address', 'applicant_name']
        for field in required_fields:
            if not application_data.get(field):
                return False
        return True

    def receive_application(self, application_data):
        """
        Accept a new application and assign an ID.
        If the application is incomplete, mark it accordingly.
        Returns an application record (as a dictionary) with assigned ID and status.
        """
        application_id = self.next_id
        self.next_id += 1
        application = {
            'id': application_id,
            'data': application_data,
            'status': 'Received'
        }
        # Check completeness of the submission
        if not self.check_completeness(application_data):
            # Mark as incomplete and require additional info
            application['status'] = 'Incomplete'
            application['notes'] = 'Missing required information'
        else:
            application['status'] = 'Submitted'
            application['notes'] = 'Application complete and accepted'
        return application
