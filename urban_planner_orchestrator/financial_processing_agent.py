# financial_processing_agent.py
class FinancialProcessingAgent:
    """
    Agent responsible for handling financial transactions such as fee calculation and payments.
    """
    def __init__(self, fee_schedule=None):
        # fee_schedule can be passed in or use default values
        if fee_schedule is None:
            # Default fee schedule (could be loaded from config in a real system)
            self.fee_schedule = {
                'base_fee': 100,
                'plan_review_fee': 500,
                'hearing_fee': 200,
                'ceqa_fee': 300
            }
        else:
            self.fee_schedule = fee_schedule
        # Store payments records
        self.payments = {}

    def calculate_fees(self, application):
        """
        Calculate fees for the application based on its requirements.
        Returns a dictionary of fees and total.
        """
        fees = {}
        # Base fee (application fee)
        fees['Base Application Fee'] = self.fee_schedule.get('base_fee', 0)
        # Additional fees for required processes
        if application.get('requires_plan_review'):
            fees['Plan Review Fee'] = self.fee_schedule.get('plan_review_fee', 0)
        if application.get('requires_hearing'):
            fees['Hearing Fee'] = self.fee_schedule.get('hearing_fee', 0)
        if application.get('requires_ceqa'):
            fees['Environmental Review Fee'] = self.fee_schedule.get('ceqa_fee', 0)
        total = sum(fees.values())
        fees['Total'] = total
        application['fees_due'] = fees
        return fees

    def process_payment(self, application, amount):
        """
        Process a payment for the given application. Returns True if payment is accepted.
        """
        # In real system, integrate with payment gateway. Here just record payment.
        due = application.get('fees_due', {}).get('Total', 0)
        if amount >= due:
            # Record payment
            self.payments[application['id']] = amount
            application['fees_due']['Total'] = 0
            application['fees_paid'] = True
            application['status'] = 'Payment Received'
            return True
        else:
            # Insufficient payment (partial payment scenario)
            application['fees_paid'] = False
            return False
