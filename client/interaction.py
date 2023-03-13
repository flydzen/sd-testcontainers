import os

import aiohttp
from urllib.parse import urlencode

from base.base import Company

STOCK_URL = os.environ.get('STOCK_URL', 'http://localhost:8081')


class Interaction:
    @staticmethod
    async def buy(company_name: str, amount: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(urlencode(f'{STOCK_URL}/buy?name={company_name}&amount={amount}')) as resp:
                json = await resp.json()
                return json['expenditure']

    @staticmethod
    async def sell(company_name: str, amount: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(urlencode(f'{STOCK_URL}/sell?name={company_name}&amount={amount}')) as resp:
                json = await resp.json()
                return json['revenue']

    @staticmethod
    async def get_companies():
        async with aiohttp.ClientSession() as session:
            async with session.get(STOCK_URL) as resp:
                json = await resp.json()
                return list(map(lambda x: Company(**x), json))

    @staticmethod
    async def get_company(company_name: str) -> Company:
        async with aiohttp.ClientSession() as session:
            async with session.get(urlencode(f'{STOCK_URL}/company?name={company_name}')) as resp:
                json = await resp.json()
                return Company(**json)
