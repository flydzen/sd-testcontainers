from stock.actions.base_action import BaseAction
from stock.actions.get_company import GetCompanyAction
from base.exceptions import CompanyNotFoundError, NotEnoughSharesError


class SellSharesAction(BaseAction):
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def run(self) -> float:
        company = GetCompanyAction(name=self.name).run()
        if not company:
            raise CompanyNotFoundError
        if company.amount < self.amount:
            raise NotEnoughSharesError

        company.amount += self.amount
        self.repository.set_company(company)
        return company.price
