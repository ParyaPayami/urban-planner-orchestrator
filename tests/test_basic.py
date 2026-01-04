from urban_planner_orchestrator.admin_agent import AdminAgent
from urban_planner_orchestrator.application_intake_agent import ApplicationIntakeAgent


def test_admin_rules():
    admin = AdminAgent()
    assert 'fees' in admin.business_rules


def test_application_intake():
    intake = ApplicationIntakeAgent()
    app = intake.receive_application({'applicant_name': 'Test', 'address': '123 Main St'})
    assert app['id'] == 1
    assert app['status'] in {'Submitted', 'Incomplete'}
