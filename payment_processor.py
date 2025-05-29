class PaymentProcessor:
    def __init__(self):
        self.payment_methods = {}
        self.transactions = []

    def add_payment_method(self, user_id: str, payment_info: dict):
        """Add or update payment method for a user"""
        self.payment_methods[user_id] = payment_info

    def process_payment(self, user_id: str, amount: float) -> bool:
        """Process a payment for the given amount"""
        if user_id not in self.payment_methods:
            return False

        # Simulate payment processing
        transaction = {
            "user_id": user_id,
            "amount": amount,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
        self.transactions.append(transaction)
        return True

    def get_transaction_history(self, user_id: str) -> List[dict]:
        """Retrieve transaction history for a user"""
        return [t for t in self.transactions if t["user_id"] == user_id]