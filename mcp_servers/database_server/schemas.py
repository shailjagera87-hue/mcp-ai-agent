from pydantic import BaseModel, Field


class CustomerSearchRequest(BaseModel):

    query: str = Field(
        min_length=2,
        max_length=100
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=50
    )


class CustomerIDRequest(BaseModel):

    customer_id: int = Field(
        gt=0
    )