from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class CurrencyConversionRequest(BaseModel):
    amount: Decimal = Field(
        gt=0,
        le=Decimal("1000000000")
    )

    from_currency: str = Field(
        min_length=3,
        max_length=3
    )

    to_currency: str = Field(
        min_length=3,
        max_length=3
    )

    @field_validator("from_currency", "to_currency")
    @classmethod
    def validate_currency(cls, value):
        return value.upper()


class ExchangeRateRequest(BaseModel):
    from_currency: str = Field(
        min_length=3,
        max_length=3
    )

    to_currency: str = Field(
        min_length=3,
        max_length=3
    )

    @field_validator("from_currency", "to_currency")
    @classmethod
    def validate_currency(cls, value):
        return value.upper()