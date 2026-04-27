from flask import Flask, request, jsonify
# We import your "Brain" from the other file
from transaction_models import Transaction, InternationalTransaction, ComplianceError

app = Flask(__name__)

@app.route("/validate", methods=["POST"])
def validate_route() -> tuple:
    """
    Visa Validation API.
    Expects JSON: {"amount": 100.0, "merchant": "Nike", "Country": "USA"}
    """
    data = request.get_json() # get_json gets requests data, and turns it into py dict

    try:
        # 1. TODO: Extract data from the JSON request

        amount = data.get("amount")
        merchant = data.get("merchant")
        country = data.get("country", "USA")
        rate = data.get("rate", 1.0)
        # 2. TODO: Logic to decide which object to create
        # Hint: If country is not "USA", create an InternationalTransaction object
        # Otherwise, create a standard Transaction.
        # amount, merchant
        # amount, merchant, country, rate

        if country != "USA":
            print(country)
            transaction = InternationalTransaction(amount, merchant, country, rate)
        else:
            transaction = Transaction(amount, merchant)

        # 3. TODO: Run .validate() on the object
        transaction.validate()

        return jsonify({
            "status": "Success",
            "transaction_status": "Validated",
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


