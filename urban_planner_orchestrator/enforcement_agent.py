# enforcement_agent.py
class EnforcementAgent:
    """
    Agent responsible for handling investigations and enforcement cases.
    Manages complaints and code enforcement actions.
    """
    def __init__(self):
        # Simple storage for open enforcement cases
        self.cases = []
        self.next_case_id = 1

    def open_case(self, address, issue_description):
        """
        Open a new enforcement case for a given address and issue.
        Returns a case record (dict).
        """
        case = {
            'case_id': self.next_case_id,
            'address': address,
            'issue': issue_description,
            'status': 'Open',
            'assigned_to': None
        }
        self.cases.append(case)
        self.next_case_id += 1
        return case

    def assign_investigator(self, case):
        """
        Assign an investigator or inspector to the case.
        """
        # Dummy assignment logic: always assign to "Inspector A"
        case['assigned_to'] = 'Inspector A'
        case['status'] = 'Assigned'
        return case['assigned_to']

    def close_case(self, case, resolution):
        """
        Close the enforcement case with a resolution.
        """
        case['status'] = 'Closed'
        case['resolution'] = resolution
        return True
