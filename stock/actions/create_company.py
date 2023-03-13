from stock.actions.base_action import BaseAction
from stock.repository import Company


class CreateCompanyAction(BaseAction):
    def __init__(self, name: str, price: float, amount: int):
        self.name = name
        self.price = price
        self.amount = amount

    def run(self) -> None:
        company = Company(name=self.name, price=self.price, amount=self.amount)
        self.repository.set_company(company)
