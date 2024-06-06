from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.views.api_models.base_api_model import StandartResponse


class CoinQuoteItem(BaseModel):
    coin_abbreviation: str
    coin_name: Optional[str] = None
    price: Optional[float] = None
    direct_vol: Optional[float] = None
    total_vol: Optional[float] = None
    top_tier_vol: Optional[float] = None
    market_cap: Optional[float] = None
    score: Optional[str] = None
    last_7_days_price: Optional[List[float]] = None
    delta_24h_price: Optional[float] = None


class UpdateCoinVisibility(BaseModel):
    coin_id: UUID
    is_visible: bool


class AddCoin(BaseModel):
    coin_abbreviation: str  # can be more than 3 characters long


class CoinQuoteResponse(StandartResponse):
    pass
