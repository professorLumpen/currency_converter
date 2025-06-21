from pydantic import BaseModel, Field


class CurrenciesIn(BaseModel):
    currencies: str = Field(...)
    source: str = Field("USD", description="Initial currency")
    count: int = Field(1, description="Amount of initial currency")


class CurrenciesOut(BaseModel):
    currencies_rates: dict[str, float] = Field(...)


class CurrenciesList(BaseModel):
    currencies: dict[str, str] = Field(...)
