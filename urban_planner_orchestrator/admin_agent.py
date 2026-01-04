# admin_agent.py
class AdminAgent:
    """
    Agent responsible for administration and configuration of system rules and settings.
    Holds configurable business rules for workflows.
    """
    def __init__(self):
        # Define business rules (could be loaded from a config file or database in a real system)
        self.business_rules = {
            'project_types': {
                'simple': {'plan_review': False, 'hearing': False, 'ceqa': False},
                'major':  {'plan_review': True,  'hearing': True,  'ceqa': True}
            },
            'hearing_types': {
                'major': 'Planning Commission Hearing',
                'simple': None
            },
            'fees': {
                'base_fee': 100,
                'plan_review_fee': 500,
                'hearing_fee': 200,
                'ceqa_fee': 300
            }
        }

    def requires_plan_review(self, application):
        """
        Determine if the application requires a plan review based on business rules.
        """
        proj_type = application['data'].get('project_type', 'simple')
        return self.business_rules['project_types'].get(proj_type, {}).get('plan_review', False)

    def requires_hearing(self, application):
        """
        Determine if the application requires a public hearing.
        """
        proj_type = application['data'].get('project_type', 'simple')
        return self.business_rules['project_types'].get(proj_type, {}).get('hearing', False)

    def requires_ceqa(self, application):
        """
        Determine if the application requires CEQA environmental review.
        """
        proj_type = application['data'].get('project_type', 'simple')
        return self.business_rules['project_types'].get(proj_type, {}).get('ceqa', False)

    def get_fee_schedule(self):
        """
        Get the configured fee schedule.
        """
        return self.business_rules.get('fees', {})
