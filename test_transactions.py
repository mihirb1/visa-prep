import pytest
from transaction_models import Transaction, InternationalTransaction, ComplianceError

def test_valid_domestic_transaction():
    """Test that a standard valid transaction works and sets status to Validated."""
    t = Transaction(100.0, "Nike")
    t.validate()
    assert t.status == "Validated"

def test_negative_amount_error():
    """Test that a negative amount raises a ValueError."""
    t = Transaction(-50.0, "Scammer")
    # use pytest.raises to check for unexpected errors

    with pytest.raises(ValueError):
        t.validate()

def test_international_sanction_blocked():
    """Test that Iran is blocked and raises ComplianceError."""
    t = InternationalTransaction(5.0, "Adidas", "Iran", 1.0)

    with pytest.raises(ComplianceError):
        t.validate()