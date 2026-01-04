# orchestrator.py
# Main orchestrator that coordinates all agents to execute the city planning workflow.
from .admin_agent import AdminAgent
from .application_intake_agent import ApplicationIntakeAgent
from .permit_eligibility_agent import PermitEligibilityAgent
from .licensing_agent import LicensingAgent
from .gis_agent import GISAgent
from .plan_review_agent import PlanReviewAgent
from .environmental_review_agent import EnvironmentalReviewAgent
from .hearing_scheduling_agent import HearingSchedulingAgent
from .document_generation_agent import DocumentGenerationAgent
from .notification_agent import NotificationAgent
from .financial_processing_agent import FinancialProcessingAgent
from .enforcement_agent import EnforcementAgent
from .county_filing_agent import CountyFilingAgent

def main():
    # Initialize agents
    admin_agent = AdminAgent()
    intake_agent = ApplicationIntakeAgent()
    eligibility_agent = PermitEligibilityAgent()
    licensing_agent = LicensingAgent()
    gis_agent = GISAgent()
    plan_review_agent = PlanReviewAgent()
    env_agent = EnvironmentalReviewAgent()
    hearing_agent = HearingSchedulingAgent()
    doc_agent = DocumentGenerationAgent()
    notif_agent = NotificationAgent()
    financial_agent = FinancialProcessingAgent(admin_agent.get_fee_schedule())
    enforcement_agent = EnforcementAgent()
    county_agent = CountyFilingAgent()

    # Example application submission (input data)
    application_data = {
        'applicant_name': 'John Doe',
        'contact_email': 'john.doe@example.com',
        'address': '123 Main St',
        'project_type': 'major',  # 'major' will trigger plan review, hearing, CEQA
        'contractor_license': 'ABCD1234'
    }
    print("Submitting application:", application_data)
    # Application Intake
    application = intake_agent.receive_application(application_data)
    print(f"Application ID {application['id']} intake status: {application['status']}")
    if application['status'] == 'Incomplete':
        # Human-in-the-loop: prompt for missing info
        print("Application is incomplete, requesting additional information from applicant.")
        input("** Action: Applicant provides missing information (press Enter to continue) **")
        # Here we simulate that missing information is now provided:
        application['data']['address'] = application_data['address'] or "UNKNOWN"
        application['status'] = 'Submitted'
        application['notes'] = 'Application complete after resubmission'
        print("Application resubmitted and now complete.")

    # Verify contractor license
    if not licensing_agent.verify_license(application):
        print("Contractor license not verified. Prompting for license registration.")
        input("** Action: Applicant obtains/updates license (press Enter to continue) **")
        # Simulate registering a new license
        licensing_agent.register_license(application, {'license_number': 'NEWLICENSE'})
        print("License registered:", application['data']['contractor_license'])

    # Determine permit eligibility and required steps
    eligible = eligibility_agent.evaluate_application(application, admin_agent, gis_agent)
    if not eligible:
        print("Application is not eligible to proceed. Ending process.")
        return
    print("Application is eligible for processing.")

    # Calculate initial fees
    fees = financial_agent.calculate_fees(application)
    print("Calculated fees:", fees)
    # Request payment (human-in-the-loop)
    input(f"** Action: Applicant pays fees (Total = ${fees['Total']}) (press Enter once paid) **")
    financial_agent.process_payment(application, fees['Total'])
    print("Payment status:", "Paid" if application.get('fees_paid') else "Unpaid")

    # Perform Plan Review (if required)
    if application.get('requires_plan_review'):
        print("Routing to plan review...")
        review_result = plan_review_agent.perform_review(application)
        print("Plan review outcome:", review_result)
        if review_result == 'corrections_required':
            # Human-in-the-loop: wait for resubmission of corrected plans
            print("Plan review identified issues. Applicant must resubmit corrected plans.")
            input("** Action: Applicant submits revised plans (press Enter to continue) **")
            # Re-run plan review on resubmission
            review_result = plan_review_agent.perform_review(application, resubmission=True)
            print("Plan review outcome after resubmission:", review_result)
        if review_result != 'approved':
            print("Plan review not approved. Cannot proceed to hearing.")
            return
    else:
        print("Plan review not required for this application.")

    # Conduct Environmental Review (CEQA) if required
    if application.get('requires_ceqa'):
        print("Conducting environmental review (CEQA)...")
        env_agent.conduct_review(application)
        print("Environmental review status:", application.get('environmental_status'))
        # In a real scenario, there might be a public comment period or approval needed here.

    # Schedule Hearing if required
    if application.get('requires_hearing'):
        hearing_date = hearing_agent.schedule_hearing(application)
        print(f"Hearing scheduled on {hearing_date.date()} for application {application['id']}")
        # Generate hearing notice and send notifications
        notice_doc = doc_agent.generate_document("HearingNotice", application)
        nearby_addresses = gis_agent.get_nearby_addresses(application['data']['address'])
        print("Generated hearing notice. Notifying nearby properties and applicant...")
        notif_agent.send_notifications(nearby_addresses, notice_doc)
        notif_agent.send_notification(application['data']['contact_email'], notice_doc)
        # Human-in-the-loop: wait for hearing to occur and get outcome
        decision = input("** Action: Hearing held. Enter hearing outcome (Approved/Denied) ** ")
        hearing_agent.record_outcome(application, decision)
        print("Hearing outcome recorded as:", application.get('hearing_outcome'))
    else:
        print("No public hearing required for this application.")
        # If no hearing, we can consider it approved by staff if applicable
        application['status'] = 'Approved'

    # Generate decision document and notify applicant
    if application['status'] in ['Approved', 'Denied']:
        decision_doc = doc_agent.generate_document("DecisionLetter", application)
        notif_agent.send_notification(application['data']['contact_email'], decision_doc)
        print("Sent decision notification to applicant.")
    # If approved, issue permit and perform final steps
    if application['status'] == 'Approved':
        permit_doc = doc_agent.generate_document("PermitCertificate", application)
        notif_agent.send_notification(application['data']['contact_email'], permit_doc)
        county_agent.file_record(application)
        print("Permit issued and filed with county records.")
    elif application['status'] == 'Denied':
        print("Application was denied. No permit issued.")
    else:
        print("Application status after hearing:", application['status'])

    # --- Enforcement scenario example ---
    # (This part is separate from the above permit workflow, demonstrating enforcement agent usage)
    print("\nNow simulating an enforcement scenario...")
    case = enforcement_agent.open_case("456 Oak Ave", "Unpermitted construction")
    print(f"Enforcement case opened for {case['address']} (Issue: {case['issue']})")
    investigator = enforcement_agent.assign_investigator(case)
    print(f"Assigned {investigator} to enforcement case {case['case_id']}")
    # Generate violation notice and notify property owner
    violation_doc = doc_agent.generate_document("ViolationNotice", case)
    notif_agent.send_notification(f"Owner of {case['address']}", violation_doc)
    # Close the case after resolution
    enforcement_agent.close_case(case, "Permit obtained for construction")
    print(f"Enforcement case {case['case_id']} closed with resolution: {case.get('resolution')}")

if __name__ == "__main__":
    main()
