class Transaction:
    def __init__(self, amount: float, merchant: str):
        """Initalizes the transaction with data."""
        self.amount = amount
        self.merchant = merchant
        self.status = "Pending" # All transactions start as Pending

    def validate(self):
        """
        YOUR WORK:
        1. Check if self.amount is a number (isinstance). If not, raise TypeError.
        2. If self.amount <= 0, raise a ValueError with a helpful message.
        3. If it passes both, change self.status to 'Validated'.
        """
        if not isinstance(self.amount, (int, float)):
            raise TypeError(f"Amount should be a number, it is {type(self.amount)}")
        elif self.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        else:
            self.status = 'Validated'
    
    def __str__(self):
        """This defines how the object looks when you print it."""
        return f"Transaction({self.merchant}, ${self.amount}, Status: {self.status})"

class InternationalTransaction(Transaction):
    def __init__(self, amount: float, merchant: str, country: str, exchange_rate: float):
        # 1. Use 'super()' to let the original Transaction class handle amount and merchant
        super().__init__(amount, merchant)
        self.country = country
        self.exchange_rate = exchange_rate

    def convert_currency(self):
        """Calculates the amount in USD."""
        self.amount = self.amount * self.exchange_rate
        print(f"Converted {self.merchant} transaction from {self.country} to USD.")

    def validate(self):
        # 1. Run the standard parent checks (amount > 0, etc.)
        super().validate()

        # 2. Add custom compliance check
        sanctioned_countries = ["North Korea", "Iran"]
        if self.country in sanctioned_countries:
            self.status = "Blocked"
            # We raise an error so the 'batch' loop knows this failed
            raise ValueError(f"Compliance Alert: Transaction from {self.country} blocked")

if __name__ == "__main__":
    # 2. Create a list of Transaction objections

    t_intl = InternationalTransaction(100.0, "Adidas", "Germany", 1.08)
    print(f"Before Conversion: {t_intl}")

    t_intl.convert_currency()
    t_intl.validate()
    print(f"After Conversion & Validation: {t_intl}")

    t_us = Transaction(200.0, "Samsung")
    print(t_us.validate())
    t_itl = InternationalTransaction(500.0, "LocalShop", "North Korea", 1.0)
    try:
        t_itl.validate()
    except ValueError as e:
        print(f"{e}")