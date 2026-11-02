from pydantic import BaseModel, Field


class WeatherRequest(BaseModel):
    city: str = Field(
        min_length=2,
        max_length=100,
        description="Name of the city"
    )


class ForecastRequest(BaseModel):
    city: str = Field(
        min_length=2,
        max_length=100
    )

    days: int = Field(
        default=3,
        ge=1,
        le=7,
        description="Number of forecast days"
    )