from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import select

from app.models.coinquotes_models.coinquotes_model import CoinQuoteModel
from app.models.session import get_session


class CoinQuotesController:
    @classmethod
    async def get_visible_coinquotes(cls) -> List[CoinQuoteModel]:
        async with get_session() as session:
            result = await session.execute(
                select(CoinQuoteModel).where(CoinQuoteModel.is_visible is True)
            )
            return result.scalars().all()

    @classmethod
    async def update_coin_visibility(cls, coin_id: UUID, is_visible: bool) -> None:
        async with get_session() as session:
            coin_quote = await session.get(CoinQuoteModel, coin_id)
            if coin_quote:
                coin_quote.is_visible = is_visible
                await session.commit()
                return

    @classmethod
    async def add_coin_quote(cls, coin_abbreviation: str) -> None:
        async with get_session() as session:
            coin_quote = CoinQuoteModel(id=uuid4(), coin_abbreviation=coin_abbreviation)

            session.add(coin_quote)
            await session.commit()
            return

    @classmethod
    async def get_by_coin_abbreviation(
        cls, coin_abbreviation: str
    ) -> Optional[CoinQuoteModel]:
        async with get_session() as session:
            result = await session.execute(
                select(CoinQuoteModel).where(
                    CoinQuoteModel.coin_abbreviation == coin_abbreviation
                )
            )
            return result.scalar_one_or_none()

    # @classmethod
    # async def get_by_id(cls, coin_id: str) -> Optional[CoinQuoteModel]:
    #     async with get_session() as session:
    #         result = await session.execute(
    #             select(CoinQuoteModel).where(CoinQuoteModel.id == coin_id)
    #         )
    #         return result.scalar_one_or_none()
