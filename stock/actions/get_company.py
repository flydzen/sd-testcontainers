from stock.actions.base_action import BaseAction
from stock.repository import Company


class GetCompanyAction(BaseAction):
    def __init__(self, name: str):
        self.name = name

    def run(self) -> Company:
        return self.repository.get_company(self.name)
