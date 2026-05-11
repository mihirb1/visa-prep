import sqlite3
from transaction_models import Transaction
from sqlite3 import IntegrityError

def save_transaction(transaction: Transaction) -> None:  
    '''
    Takes in a transaction object (validated) from app.py, inserts its data into SQL
    '''
    with sqlite3.connect("visa_ledger.db") as conn:
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions(amount, merchant_id, country, rate, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (transaction.amount, transaction.merchant.merchant_id,
                getattr(transaction, "country", "USA"),
                getattr(transaction, "rate", 1.0),
                transaction.status)
            )
            # for validated transactions, update merchant balance (allow it to go through)
            if transaction.status == 'Validated':
                cursor.execute('''
                    UPDATE merchants
                    SET balance = balance + ?
                    WHERE id = ?
                ''', (transaction.amount, transaction.merchant.merchant_id))
        except IntegrityError as e:
            raise IntegrityError(e)

def get_or_create_merchant(merchant: str, category: str="General", risk_level: float=0.1) -> dict:
    '''
    Searches for merchant name in 'merchants' table in database.
    If name does not exist, create a new row for that specific merchant
    Return {id, category, risk_level} of merchant row regardless.
    '''
    #  validates merchant name before we insert into database
    if not isinstance(merchant, str):
        raise TypeError("Merchant name must be a string")

    elif merchant.strip() == "":
        raise ValueError("Merchant name can not be empty")

    with sqlite3.connect("visa_ledger.db") as conn:
        try:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, category, risk_level
                FROM merchants
                WHERE name = ?
            ''', (merchant,))

            result = cursor.fetchone() # returns result from select, which is either
                                # a tuple with result, or None

            if result:
                return {"id": result[0], "category": result[1], "risk_level": result[2]}
            else:
                cursor.execute('''
                    INSERT INTO merchants (name, category, risk_level)
                    VALUES (?, ?, ?)
                ''', (merchant, category, risk_level))

                return {"id": cursor.lastrowid, "category": category, "risk_level": risk_level}
        except IntegrityError as e:
            raise IntegrityError(e)


