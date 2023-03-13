import os

import aiohttp

from base.base import Company
from base.exceptions import InteractionError

STOCK_URL = os.environ.get('STOCK_URL', 'http://localhost:8081')


class Interaction:
    @staticmethod
    async def buy(company_name: str, amount: int):
        q = f'{STOCK_URL}/buy?name={company_name}&amount={amount}'
        async with aiohttp.ClientSession() as session:
            async with session.post(q) as resp:
                if resp.status != 200:
                    raise InteractionError(resp.status, 'buy', await resp.text())
                json = await resp.json()
                return json['expenditure']

    @staticmethod
    async def sell(company_name: str, amount: int):
        q = f'{STOCK_URL}/sell?name={company_name}&amount={amount}'
        async with aiohttp.ClientSession() as session:
            async with session.post(q) as resp:
                if resp.status != 200:
                    raise InteractionError(resp.status, 'buy', await resp.text())
                json = await resp.json()
                return json['revenue']

    @staticmethod
    async def get_companies():
        q = STOCK_URL
        async with aiohttp.ClientSession() as session:
            async with session.get(q) as resp:
                if resp.status != 200:
                    raise InteractionError(resp.status, 'buy', await resp.text())
                json = await resp.json()
                return list(map(lambda x: Company(**x), json))

    @staticmethod
    async def get_company(company_name: str) -> Company:
        q = f'{STOCK_URL}/company?name={company_name}'
        async with aiohttp.ClientSession() as session:
            async with session.get(q) as resp:
                if resp.status != 200:
                    raise InteractionError(resp.status, 'buy', await resp.text())
                json = await resp.json()
                return Company(**json)
