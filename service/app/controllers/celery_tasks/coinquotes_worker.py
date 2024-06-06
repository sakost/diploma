import asyncio
import os
from dataclasses import dataclass
from typing import List

import aiohttp
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.coinquotes_models.coinquotes_model import CoinQuoteModel
from app.models.session import get_session


load_dotenv(find_dotenv())
# from celery import Celery


# coinquotes_celery_app = Celery("tasks", broker="redis://localhost:6379/0")

COINQUOTES_API_KEY = os.environ.get("COINQUOTES_API_KEY")
HEADERS = {"Authorization": f"Apikey {COINQUOTES_API_KEY}"}


async def update_coin_name(coin: CoinQuoteModel, client: aiohttp.ClientSession):
    try:
        url = f"https://data-api.cryptocompare.com/asset/v1/data/by/symbol?asset_symbol={coin.coin_abbreviation}"
        async with client.get(url, headers=HEADERS) as response:
            response_data = await response.json()
            coin.coin_name = response_data.get("Data").get("NAME")
    except (aiohttp.ClientError, KeyError) as e:
        print(f"Error updating coin name: {e}")


async def update_symbols_full_data(coin: CoinQuoteModel, client: aiohttp.ClientSession):
    try:
        url = f"https://min-api.cryptocompare.com/data/pricemultifull?fsyms={coin.coin_abbreviation}&tsyms=USD"
        async with client.get(url, headers=HEADERS) as response:
            response_data = await response.json()
            info = response_data.get("RAW").get(coin.coin_abbreviation).get("USD")
            coin.price = info.get("PRICE")
            coin.direct_vol = info.get("VOLUME24HOURTO")
            coin.total_vol = info.get("TOTALVOLUME24HTO")
            coin.top_tier_vol = info.get("TOPTIERVOLUME24HOURTO")
            coin.market_cap = info.get("MKTCAP")
            coin.delta_24h_price = info.get("CHANGEPCT24HOUR")
    except (aiohttp.ClientError, KeyError) as e:
        print(f"Error updating coin data: {e}")


async def update_coins_info(coins: List[CoinQuoteModel], session: AsyncSession):
    async with aiohttp.ClientSession() as client:
        tasks = []
        for coin in coins:
            if not coin.coin_name:
                tasks.append(update_coin_name(coin=coin, client=client))
            tasks.append(update_symbols_full_data(coin=coin, client=client))
        await asyncio.gather(*tasks)
        await session.commit()


# @coinquotes_celery_app.task
async def update_coin_quotes():
    async with get_session() as session:
        result = await session.execute(select(CoinQuoteModel))
        coins = result.scalars().all()
        await update_coins_info(coins=coins, session=session)


async def main():
    await update_coin_quotes()


# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())


@dataclass
class Coin:
    abbreviation: str
    coin_name: str
    price: float
    direct_vol: float
    total_vol: float
    top_tier_vol: float
    market_cap: float
    score: float  # not done
    last_7_days_price: float  # not done
    delta_24h_price: str
    is_visible: bool
