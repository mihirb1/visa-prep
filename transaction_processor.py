def process_transaction(amount: float, merchant: str) -> str:
    """
    Validates and processes a single transaction

    # YOUR WORK HERE:
    # 1. If it is less than or equal to 0, raise a ValueError with a message.
    # 2. Otherwise, return a string that says: "Success: [merchant] charged [amount]
    """
    # New "Pro" check:
    if not isinstance(amount, (int, float)):
        raise TypeError(f"Invalid type for amount: {type(amount)}. Expected a number.")
    if amount <= 0:
        raise ValueError(f"Merchant {merchant} failed due " \
        "to transaction amount <= 0")
    else:
        return f"Success: {merchant} charged {amount}"

# Test the function below:

if __name__ == "__main__":
    # A list of 'batches' (amount, merchant)

    transactions = [
        (100.0, "Nike"),
        (-5.0, "Target"),
        (250.50, "Apple"), 
        (0.0, "Unknown"),
        ("one hundred", "Scammer")
    ]

    for amt, mch in transactions:
        try:
            # 1. call the function and SAVE the result to a variable
            # 2. Print that result
            transaction_status = process_transaction(amt, mch)
            print(transaction_status)

        except ValueError as e:
            # 3. Print a message saying which merchant failed and why
            print(f"{e}")
        
        except TypeError as e:
            print(f"System error: {e}")