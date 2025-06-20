from abc import ABC, abstractmethod

import httpx
from fastapi import HTTPException

from app.core.config import settings


class AbstractCurrencyService(ABC):
    @abstractmethod
    async def get_currencies_rate(self, currencies_list: list[str], source: str, count: int) -> dict[str, float]:
        pass

    @abstractmethod
    async def get_currencies_list(self) -> dict[str, str]:
        pass


class CurrencyLayerService(AbstractCurrencyService):
    def __init__(self, api_link: str = settings.CURRENCY_API_LINK, list_link: str = settings.CURRENCY_API_LIST):
        self.api_link = api_link
        self.list_link = list_link
        self.client = httpx.AsyncClient()

    async def get_currencies_rate(
        self, currencies_list: list[str], source: str = "USD", count: int = 1
    ) -> dict[str, float]:
        url = f"{self.api_link}&currencies={','.join(currencies_list)}&source={source}&format={count}"
        response = await self.client.get(url)
        response.raise_for_status()
        quotes = response.json().get("quotes")
        if not quotes:
            raise HTTPException(status_code=404, detail="No quotes found")
        return quotes

    async def get_currencies_list(self) -> dict[str, str]:
        url = self.list_link
        response = await self.client.get(url)
        response.raise_for_status()
        currencies = response.json().get("currencies")
        if not currencies:
            raise HTTPException(status_code=404, detail="No currencies found")
        return currencies


def get_currency_service() -> AbstractCurrencyService:
    return CurrencyLayerService()
