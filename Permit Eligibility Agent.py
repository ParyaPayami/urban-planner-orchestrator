# permit_eligibility_agent.py
class PermitEligibilityAgent:
    """
    Agent responsible for determining permit eligibility and necessary process steps for an application.
    It evaluates the application against zoning rules and business rules to decide required reviews.
    """
    def evaluate_application(self, application, admin_agent, gis_agent):
        """
        Evaluate the application for eligibility and determine required further steps.
        Updates the application record with flags for plan review, hearing, CEQA, etc.
        Returns True if eligible, False if ineligible.
        """
        # Basic eligibility check: verify address is valid within jurisdiction
        parcel_info = gis_agent.verify_address(application['data'].get('address'))
        if not parcel_info:
            # Address not valid or not in city
            application['status'] = 'Invalid Address'
            application['notes'] = 'Address outside jurisdiction or not found'
            return False
        else:
            # Save parcel info (like parcel id, zoning) into application for reference
            application['parcel'] = gis_agent.get_parcel_info(application['data']['address'])
        # Placeholder: integrate Azure AI Foundry to assess zoning or similar knowledge-based checks
        # Determine required process steps using admin/business rules
        application['requires_plan_review'] = admin_agent.requires_plan_review(application)
        application['requires_hearing'] = admin_agent.requires_hearing(application)
        application['requires_ceqa'] = admin_agent.requires_ceqa(application)
        # Additional eligibility checks could go here (e.g., zoning compatibility, outstanding violations)
        # For now, assume if address is valid, the project is eligible to proceed.
        application['status'] = 'Eligible'
        return True
