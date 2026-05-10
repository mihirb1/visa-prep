from typing import List

class ComplianceError(Exception):
    """Raised for 2 main reasons:
        When a transaction violates international financial regulations.
        When the merchant in a transaction has too high of a risk level.
    """
    pass

class Merchant:
    def __init__(self, merchant_id: int, merchant_name: str, category: str, risk_level: float):
        """
        Initializes a Merchant instance.

        Args:
            merchant_id: ID of the merchant, which used as a foreign key in the 'transactions' table
            merchant_name: name of the Merchant
            category: type of sales the Merchant makes (ex. clothing, sporting, general)
            risk_level: trustworthiness of Merchant, from 0 to 1 (inclusive)

        """
        self.merchant_id: int = merchant_id
        self.merchant_name: str = merchant_name
        self.category: str = category
        self.risk_level: float = risk_level

    def validate(self) -> None:
        """Checks validatity of merchant name.

        Raises: 
            TypeError: if merchant_name is not of type string.
            ValueError: if merchant_name is blank when stripped of whitespace.
        """
        if not isinstance(self.merchant_name, str):
            raise TypeError("Merchant name must be a string")
        elif self.merchant_name.strip() == "":
            raise ValueError("Merchant name can not be null")

class Transaction:
    def __init__(self, amount: float, merchant: Merchant) -> None:
        """Initializes a base Visa transaction.

        Args:
            amount: The value of the transaction.
            merchant: The merchant object, which has merchant id, name, category, and risk_level
        """
        self.amount: float = amount
        self.merchant: Merchant = merchant
        self.status: str = "Pending"

    def validate(self) -> None:
        """Validates the transaction data integrity.

        Raises:
            TypeError: If amount is not numeric.
            ValueError: If amount is zero or negative.
            ComplianceError: If merchant has too high of a risk_level.
        """
        if self.merchant.risk_level > 0.3:
            self.status = "Blocked"
            raise ComplianceError("High risk merchant")
        elif not isinstance(self.amount, (float, int)):
            raise TypeError("Amount must be numeric")
        elif self.amount <= 0:
            raise ValueError("Amount must be positive")
        else:
            self.status = "Validated"

    def __str__(self) -> str:
        return f"Transaction({self.merchant_id}, ${self.amount}, Status: {self.status})"

class InternationalTransaction(Transaction):
    def __init__(self, amount: float, merchant: Merchant, country: str, rate: float) -> None:
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
