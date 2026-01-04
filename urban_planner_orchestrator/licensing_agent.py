# licensing_agent.py
class LicensingAgent:
    """
    Agent responsible for managing licensing and registration, such as contractor licenses or business licenses.
    """
    def __init__(self):
        # Dummy license database (e.g., contractor licenses) as a set of valid license numbers
        self.valid_licenses = {"ABCD1234", "XYZ7890"}

    def verify_license(self, application):
        """
        Verify that the applicant (or contractor) has a valid license.
        Returns True if valid, False if not.
        """
        license_no = application['data'].get('contractor_license')
        if license_no and license_no in self.valid_licenses:
            application['license_status'] = 'Verified'
            return True
        else:
            application['license_status'] = 'Unverified'
            return False

    def register_license(self, application, license_info):
        """
        Register a new license (or update existing) for the applicant.
        """
        # In a real system, this would create a new license entry.
        # Here we simulate by adding to valid licenses list.
        new_license_no = license_info.get('license_number', 'NEWLICENSE')
        self.valid_licenses.add(new_license_no)
        application['data']['contractor_license'] = new_license_no
        application['license_status'] = 'Verified'
        return new_license_no
