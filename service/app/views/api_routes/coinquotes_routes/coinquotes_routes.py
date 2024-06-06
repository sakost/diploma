from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate

from app.controllers.db_controllers.coinquotes_controller import CoinQuotesController
from app.utils.user_auth_handlers import get_current_user_role, requires_role
from app.views.api_models.coinquotes_api_models import (
    AddCoin,
    CoinQuoteItem,
    CoinQuoteResponse,
    UpdateCoinVisibility,
)


database_controller = CoinQuotesController()
coinquotes_router = APIRouter()


@coinquotes_router.get("/")
async def get_coin_quotes() -> Page[CoinQuoteItem]:
    # TODO: add check for user role and create new response model with is_visible param
    coin_quotes = await database_controller.get_visible_coinquotes()
    return paginate(coin_quotes)


@coinquotes_router.patch("/", response_model=CoinQuoteResponse)
async def update_coin_visibility(
    update_data: UpdateCoinVisibility,
    user_role: str = Depends(get_current_user_role),
):
    await requires_role(user_role, "admin")

    await database_controller.update_coin_visibility(
        update_data.coin_id, update_data.is_visible
    )
    return CoinQuoteResponse(
        message="Coin updated successfully", status_code=status.HTTP_204_NO_CONTENT
    )


@coinquotes_router.post("/", response_model=CoinQuoteResponse)
async def add_coin_quote(
    coin_data: AddCoin,
    user_role: str = Depends(get_current_user_role),
):
    await requires_role(user_role, "admin")
    coin_exists = await database_controller.get_by_coin_abbreviation(
        coin_data.coin_abbreviation
    )
    if not coin_exists:
        await database_controller.add_coin_quote(coin_data.coin_abbreviation)
        return CoinQuoteResponse(
            message="Coin created successfully", status_code=status.HTTP_201_CREATED
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Coin already exists"
    )
