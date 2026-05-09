import sqlite3

def save_transaction(transaction: obj) -> None:  
    '''
    Takes in a transaction object (validated) from app.py, inserts its data into SQL
    '''
    with sqlite3.connect("visa_ledger.db") as conn:
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO transactions(amount, merchant_id, country, rate, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction.amount, transaction.merchant_id,
            getattr(transaction, "country", "USA"),
            getattr(transaction, "rate", 1.0),
            transaction.status)
        )

        conn.commit()

def get_or_create_merchant(merchant: str, category: str="General", risk_level: float=0.1) -> int:
    '''
    Searches for merchant name in 'merchants' table in database.
    If name does not exist, create a new row for that specific merchant
    Return ID of merchant row regardless.
    '''
    with sqlite3.connect("visa_ledger.db") as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id
            FROM merchants
            WHERE name = ?
        ''', (merchant,))

        id = cursor.fetchone() # returns result from select, which is either
                               # a tuple with result, ie (1, ) or None

        if id:
            return id[0]
        else:
            cursor.execute('''
                INSERT INTO merchants (name, category, risk_level)
                VALUES (?, ?, ?)
            ''', (merchant, category, risk_level))

            conn.commit()

            return cursor.lastrowid
        

