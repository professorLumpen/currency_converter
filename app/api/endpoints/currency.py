from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.utils.external_api import AbstractCurrencyService, CurrencyLayerService


currency_router = APIRouter(prefix="/currency", tags=["currencies"])


@currency_router.get("/exchange/")
async def get_currencies_rate(
    currencies: str,
    source: str = "USD",
    count: int = 1,
    currency_service: AbstractCurrencyService = Depends(CurrencyLayerService),
):
    currencies_list = currencies.split(",")
    result = await currency_service.get_currencies_rate(currencies_list, source, count)
    return JSONResponse(result)


@currency_router.get("/list/")
async def get_currencies_list(currency_service: AbstractCurrencyService = Depends(CurrencyLayerService)):
    currencies_list = await currency_service.get_currencies_list()
    return currencies_list
