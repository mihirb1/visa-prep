from flask import Flask, request, jsonify
import sqlite3
# We import your "Brain" from the other file
from transaction_models import Transaction, InternationalTransaction, ComplianceError
from database_manager import save_transaction

app = Flask(__name__)

@app.route("/validate", methods=["POST"])
def validate_route() -> tuple:
    """
    Visa Validation API.
    Expects JSON: {"amount": 100.0, "merchant": "Nike", "Country": "USA", "rate": 1.0}
    """
    data = request.get_json() # get_json gets requests data, and turns it into py dict

    try:

        amount = data.get("amount")
        merchant = data.get("merchant")
        country = data.get("country", "USA")
        rate = data.get("rate", 1.0)

        if country != "USA":
            transaction = InternationalTransaction(amount, merchant, country, rate)
        else:
            transaction = Transaction(amount, merchant)

        transaction.validate()
        save_transaction(transaction)

        return jsonify({
            "status": "Success",
            "transaction_status": transaction.status,
            "merchant": merchant
        }), 200

    except ComplianceError as e:
        return jsonify({"status": "Security Alert", "message": str(e)}), 400

    except (TypeError, ValueError) as e:
        return jsonify({"status": "Data Error", "message": str(e)}), 400

    except Exception as e:
        return jsonify({"status": "System Error", "message": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)


