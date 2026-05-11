from flask import Flask, request, jsonify
import sqlite3
# We import your "Brain" from the other file
from transaction_models import Transaction, InternationalTransaction, Merchant, ComplianceError
from database_manager import save_transaction, get_or_create_merchant
from sqlite3 import IntegrityError

app = Flask(__name__)

@app.route("/validate", methods=["POST"])
def validate_route() -> tuple:
    """
    Visa Validation API.
    Expects JSON: {"amount": 100.0, "merchant": "Nike", "country": "USA", "rate": 1.0}
    """
    data = request.get_json() # get_json gets requests data, and turns it into py dict
    try:
        amount = data.get("amount")

        # finds corresponding merchant_id, category, risk_level for this merchant name 
        # (creates new row if needed)
        merchant_name = data.get("merchant")
        merchant_res = get_or_create_merchant(merchant_name) 

        country = data.get("country", "USA")
        rate = data.get("rate", 1.0)

        # validate merchant
        merchant = Merchant(
            merchant_id = merchant_res["id"],
            merchant_name = merchant_name,
            category = merchant_res["category"],
            risk_level = merchant_res["risk_level"]
        )
        merchant.validate()

        # validate transaction, since merchant is valid
        if country != "USA":
            transaction = InternationalTransaction(amount, merchant, country, rate)
        else:
            transaction = Transaction(amount, merchant)

        transaction.validate()
        save_transaction(transaction)

        return jsonify({
            "status": "Success",
            "transaction_status": transaction.status,
            "merchant": merchant_name,
            "merchant_id": merchant.merchant_id
        }), 200
        
    except IntegrityError as e:
        return jsonify({"status": "Database Error", "message": str(e)}), 500

    except ComplianceError as e:
        save_transaction(transaction)
        return jsonify({"status": "Security Alert", "message": str(e)}), 400

    except (TypeError, ValueError) as e:
        return jsonify({"status": "Data Error", "message": str(e)}), 400

    except Exception as e:
        return jsonify({"status": "System Error", "message": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)


