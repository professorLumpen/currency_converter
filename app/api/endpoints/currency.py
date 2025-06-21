from fastapi import APIRouter, Depends

from app.api.schemas.currency import CurrenciesIn, CurrenciesList, CurrenciesOut
from app.core.security import get_current_user
from app.db.models import User
from app.utils.external_api import AbstractCurrencyService, CurrencyLayerService


currency_router = APIRouter(prefix="/currency", tags=["currencies"])


@currency_router.get("/exchange/", response_model=CurrenciesOut)
async def get_currencies_rate(
    params: CurrenciesIn = Depends(),
    currency_service: AbstractCurrencyService = Depends(CurrencyLayerService),
    user: User = Depends(get_current_user),
):
    currencies_list = params.currencies.split(",")
    result = await currency_service.get_currencies_rate(currencies_list, params.source, params.count)
    return {"currencies_rates": result}


@currency_router.get("/list/", response_model=CurrenciesList)
async def get_currencies_list(
    currency_service: AbstractCurrencyService = Depends(CurrencyLayerService), user: User = Depends(get_current_user)
):
    currencies_list = await currency_service.get_currencies_list()
    return currencies_list
