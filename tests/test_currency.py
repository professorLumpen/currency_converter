from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_get_protected_resources(async_client):
    expected_response = {"detail": "Not authenticated"}

    response = await async_client.get("/currency/exchange/")
    assert response.status_code == 401
    assert response.json() == expected_response

    response = await async_client.get("/currency/list/")
    assert response.status_code == 401
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_wrong_token(async_client, test_token):
    headers = {"Authorization": f"Bearer {test_token}1"}
    expected_response = {"detail": "Invalid token"}

    response = await async_client.get("/currency/exchange/", headers=headers)
    assert response.status_code == 401
    assert response.json() == expected_response

    response = await async_client.get("/currency/list/", headers=headers)
    assert response.status_code == 401
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_currency_list(async_client, test_token):
    with patch(
        "app.utils.external_api.CurrencyLayerService.get_currencies_list", new_callable=AsyncMock
    ) as currency_list_mock:
        result = {"currencies": {"RUB": "RUSSIAN", "EUR": "Euro"}, "more info": "optional"}
        currency_list_mock.return_value = result

        response = await async_client.get("/currency/list/", headers={"Authorization": f"Bearer {test_token}"})
        assert response.status_code == 200
        assert response.json()["currencies"] == result["currencies"]
        currency_list_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_currency_rates(async_client, test_token):
    currency_rates = {"USD": 12.0, "EUR": 10.3, "RUB": 9.5, "JPY": 8.23}
    default_args = [list(currency_rates), "USD", 1]
    url = f"/currency/exchange/?currencies={','.join(currency_rates)}"

    with patch(
        "app.utils.external_api.CurrencyLayerService.get_currencies_rate", new_callable=AsyncMock
    ) as currency_rate_mock:
        currency_rate_mock.return_value = currency_rates

        response = await async_client.get(url, headers={"Authorization": f"Bearer {test_token}"})

        assert response.status_code == 200
        assert response.json()["currencies_rates"] == currency_rates
        currency_rate_mock.assert_awaited_once_with(*default_args)


@pytest.mark.asyncio
async def test_currency_rates_without_currencies(async_client, test_token):
    url = "/currency/exchange/"

    response = await async_client.get(url, headers={"Authorization": f"Bearer {test_token}"})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"
