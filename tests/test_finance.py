import pytest

from pydantic import ValidationError

from mcp_servers.finance_server.tools import (
    convert_currency,
    get_exchange_rate,
)


def test_currency_conversion():

    result = convert_currency(
        amount=100,
        from_currency="USD",
        to_currency="INR"
    )

    assert result["success"] is True
    assert result["converted_amount"] == "8850.00"


def test_exchange_rate():

    result = get_exchange_rate(
        from_currency="USD",
        to_currency="INR"
    )

    assert result["success"] is True
    assert result["exchange_rate"] == "88.50"


def test_reverse_exchange_rate():

    result = get_exchange_rate(
        from_currency="INR",
        to_currency="USD"
    )

    assert result["success"] is True
    assert float(result["exchange_rate"]) > 0


def test_unsupported_currency():

    result = convert_currency(
        amount=100,
        from_currency="USD",
        to_currency="XYZ"
    )

    assert result["success"] is False
    assert result["error"] == "UNSUPPORTED_CURRENCY"


def test_negative_amount():

    with pytest.raises(ValidationError):

        convert_currency(
            amount=-100,
            from_currency="USD",
            to_currency="INR"
        )


def test_same_currency_conversion():

    result = convert_currency(
        amount=100,
        from_currency="USD",
        to_currency="USD"
    )

    assert result["converted_amount"] == "100.00"