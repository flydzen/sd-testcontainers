from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from stock.actions.base_action import BaseAction
from stock.repository import StockRepository
from stock.repository import Company
from stock.actions.buy_shares import BuySharesAction
from stock.actions.create_company import CreateCompanyAction
from stock.actions.fill_company import FillCompanyAction
from stock.actions.get_companies import GetCompaniesAction
from stock.actions.get_company import GetCompanyAction
from stock.actions.sell_shares import SellSharesAction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

repository = StockRepository()
BaseAction.repository = repository


@app.get('/')
async def full_info() -> list[Company]:
    return GetCompaniesAction().run()


@app.post('/company')
async def create_company(name: str, price: float, amount: int = 0) -> None:
    return CreateCompanyAction(name, price, amount).run()


@app.get('/company')
async def get_company(name: str) -> Company:
    return GetCompanyAction(name).run()


@app.post('/fill')
async def fill_company(name: str, amount: int) -> None:
    return FillCompanyAction(name, amount).run()


@app.post('/buy')
async def buy(name: str, amount: int) -> dict[str, float]:
    expenditure = BuySharesAction(name, amount).run()
    return {'expenditure': expenditure}


@app.post('/sell')
async def sell(name: str, amount: int) -> dict[str, float]:
    revenue = SellSharesAction(name, amount).run()
    return {'revenue': revenue}
