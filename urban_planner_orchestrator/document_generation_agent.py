# document_generation_agent.py
class DocumentGenerationAgent:
    """
    Agent responsible for generating documents such as notices, letters, and reports.
    Uses templates (simulated) to create content based on application data.
    """
    def generate_document(self, doc_type, application):
        """
        Generate a document of the specified type for the given application.
        Returns the content of the document as a string.
        """
        doc_content = ""
        if doc_type == "SubmissionReceipt":
            # In future, integrate with AI template service for dynamic content.
            doc_content = (f"Receipt: Application {application['id']} received from {application['data'].get('applicant_name')} "
                           f"for project type '{application['data'].get('project_type')}'.")
        elif doc_type == "HearingNotice":
            date_str = application.get('hearing_date')
            if date_str:
                date_str = application['hearing_date'].strftime("%Y-%m-%d %H:%M")
            doc_content = (f"Notice: A public hearing for Application {application['id']} (Project: {application['data'].get('project_type')}) "
                           f"is scheduled on {date_str} at City Hall.")
        elif doc_type == "DecisionLetter":
            outcome = application.get('hearing_outcome', 'Pending')
            doc_content = (f"Decision: Application {application['id']} has been {outcome}. "
                           f"Thank you, {application['data'].get('applicant_name')}, for your submission.")
        elif doc_type == "PermitCertificate":
            doc_content = (f"Permit: Permit for Application {application['id']} is officially issued. "
                           f"Project '{application['data'].get('project_type')}' is approved for construction.")
        elif doc_type == "ViolationNotice":
            # For enforcement cases, 'application' may be an enforcement case dict
            addr = application.get('address') or application['data'].get('address')
            doc_content = (f"Violation Notice: A violation has been recorded at {addr}. Please take corrective action immediately.")
        else:
            doc_content = "Document content"
        # In a real system, this would generate a file or PDF. Here we return a string.
        application['last_document'] = doc_content
        return doc_content
