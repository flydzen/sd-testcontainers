from stock.actions.base_action import BaseAction
from stock.actions.get_company import GetCompanyAction
from base.exceptions import CompanyNotFoundError


class FillCompanyAction(BaseAction):
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def run(self) -> None:
        company = GetCompanyAction(name=self.name).run()
        if not company:
            raise CompanyNotFoundError
        company.amount += self.amount
        self.repository.set_company(company)
