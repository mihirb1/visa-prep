from typing import List

class ComplianceError(Exception):
    """Raised when a transaction violates international financial regulations."""
    pass

class Transaction:
    def __init__(self, amount: float, merchant: str) -> None:
        """Initializes a base Visa transaction.

        Args:
            amount: The value of the transaction.
            merchant: The name of the entity receiving funds.
        """
        self.amount: float = amount
        self.merchant: str = merchant
        self.status: str = "Pending"

    def validate(self) -> None:
        """Validates the transaction data integrity.

        Raises:
            TypeError: If amount is not numeric.
            ValueError: If amount is zero or negative.
        """
        if not isinstance(self.amount, (float, int)):
            raise TypeError("Amount must be numeric")
        elif self.amount <= 0:
            raise ValueError("Amount must be positive")
        else:
            self.status = "Validated"

    def __str__(self) -> str:
        return f"Transaction({self.merchant}, ${self.amount}, Status: {self.status})"

class InternationalTransaction(Transaction):
    def __init__(self, amount: float, merchant: str, country: str, rate: float) -> None:
        super().__init__(amount, merchant)
        self.country: str = country
        self.rate: float = rate 

    def validate(self) -> None:
        """Checks amount integrity and regional compliance.

        Raises:
            ComplianceError: If the transaction originates from a sanctioned region.
        """
        super().validate()
        if self.country in ["North Korea", "Iran"]:
            self.status = "Blocked"
            raise ComplianceError(f"{self.country} is a landlocked country and cannot participate in transactions")

if __name__ == "__main__":
    # Test batch with mixed types and a compliance risk
    batch: List[Transaction] = [
        Transaction(100.0, "Nike"),
        InternationalTransaction(150.0, "Sony", "Japan", 1.2),
        InternationalTransaction(50.0, "Tehran Cafe", "Iran", 1.0),
        Transaction("five", "Scammer")
    ]

    print("--- Visa Batch Processing ---")
    for t in batch:
        try:
            t.validate()
            print(f"SUCCES: {t}")
        except (ValueError, TypeError) as e:
            print(f"DATA ERROR: {e}")
        except ComplianceError as e:
            print(f"SECURITY ALERT: {e}")