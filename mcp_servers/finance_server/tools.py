
from decimal import Decimal, ROUND_HALF_UP

from mcp_servers.finance_server.schemas import (
    CurrencyConversionRequest,
    ExchangeRateRequest,
)

EXCHANGE_RATES = {
    "USD": Decimal("1.00"),
    "INR": Decimal("88.50"),
    "EUR": Decimal("0.86"),
    "GBP": Decimal("0.75"),
    "JPY": Decimal("153.00"),
    "CAD": Decimal("1.40"),
    "AUD": Decimal("1.53"),
}

CURRENCY_PRECISION = {"JPY": 0}


def get_rate(from_currency, to_currency):
    if from_currency not in EXCHANGE_RATES:
        return None

    if to_currency not in EXCHANGE_RATES:
        return None

    return (
        EXCHANGE_RATES[to_currency]
        / EXCHANGE_RATES[from_currency]
    )


def get_exchange_rate(from_currency, to_currency):
    request = ExchangeRateRequest(
        from_currency=from_currency,
        to_currency=to_currency,
    )

    source = request.from_currency
    target = request.to_currency

    rate = get_rate(source, target)

    if rate is None:
        return {
            "success": False,
            "error": "UNSUPPORTED_CURRENCY",
            "message": "Currency is not supported.",
        }

    return {
        "success": True,
        "from_currency": source,
        "to_currency": target,
        "exchange_rate": str(rate),
        "data_source": "MOCK_DATA",
    }


def convert_currency(amount, from_currency, to_currency):
    request = CurrencyConversionRequest(
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency,
    )

    source = request.from_currency
    target = request.to_currency

    rate = get_rate(source, target)

    if rate is None:
        return {
            "success": False,
            "error": "UNSUPPORTED_CURRENCY",
            "message": "Currency is not supported.",
        }

    converted_amount = request.amount * rate

    precision = CURRENCY_PRECISION.get(target, 2)
    rounding_unit = Decimal("1").scaleb(-precision)

    converted_amount = converted_amount.quantize(
        rounding_unit,
        rounding=ROUND_HALF_UP,
    )

    return {
        "success": True,
        "original_amount": str(request.amount),
        "from_currency": source,
        "to_currency": target,
        "exchange_rate": str(rate),
        "converted_amount": str(converted_amount),
        "data_source": "MOCK_DATA",
    }
