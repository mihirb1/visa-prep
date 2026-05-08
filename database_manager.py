import sqlite3

def save_transaction(transaction):  
    # takes in a transaction object (validated) from app.py, inserts its data into SQL
    with sqlite3.connect("visa_ledger.db") as conn:
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO transactions(amount, merchant, country, rate, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction.amount, transaction.merchant,
            getattr(transaction, "country", "USA"),
            getattr(transaction, "rate", 1.0),
            transaction.status)
        )

        conn.commit()
