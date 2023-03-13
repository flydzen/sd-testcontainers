from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware

from client.actions.balance import BalanceAction
from client.actions.base_action import BaseAction
from client.actions.buy import BuyAction
from client.actions.fill import FillAction
from client.actions.portfolio import PortfolioAction, PortfolioResponse
from client.actions.register import RegisterAction
from client.actions.sell import SellAction
from client.actions.wallet import WalletAction
from client.repository import Repository

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

repository = Repository()
BaseAction.repository = repository


@app.get('/')
async def root() -> PlainTextResponse:
    return PlainTextResponse('Добро пожаловать на биржу!')


@app.post('/register')
async def register() -> dict[str, int]:
    res = await RegisterAction().run()
    return {'user_id': res}


@app.get('/{user_id}/wallet')
async def wallet(user_id: int) -> dict[str, float]:
    res = await WalletAction(user_id).run()
    return {'wallet': res}


@app.post('/{user_id}/fill')
async def fill(user_id: int, money_amount: int) -> None:
    await FillAction(user_id, money_amount).run()


@app.get('/{user_id}/portfolio')
async def portfolio(user_id: int) -> PortfolioResponse:
    return await PortfolioAction(user_id).run()


@app.get('/{user_id}/balance')
async def balance(user_id: int) -> dict[str, float]:
    res = await BalanceAction(user_id).run()
    return {'total_wallet': res}


@app.post('/{user_id}/buy')
async def buy(user_id: int, company_name: str, amount: int) -> dict[str, float]:
    res = await BuyAction(user_id, company_name, amount).run()
    return {'expenditure': res}


@app.post('/{user_id}/sell')
async def sell(user_id: int, company_name: str, amount: int) -> dict[str, float]:
    res = await SellAction(user_id, company_name, amount).run()
    return {'revenue': res}
