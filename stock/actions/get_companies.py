from stock.actions.base_action import BaseAction
from stock.repository import Company


class GetCompaniesAction(BaseAction):
    def run(self) -> list[Company]:
        return self.repository.get_companies()
