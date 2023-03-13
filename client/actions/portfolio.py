from dataclasses import dataclass, replace

from base.base import Company
from client.actions.base_action import BaseAction
from client.interaction import Interaction


@dataclass
class PortfolioResponse:
    wallet_balance: float
    companies: list[Company]


class PortfolioAction(BaseAction):
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def run(self) -> PortfolioResponse:
        user = self.repository.get_user(self.user_id)
        companies = await Interaction.get_companies()

        result_companies = []
        for company in companies:
            if company.name in user.portfolio:
                result_companies.append(replace(company, amount=user.portfolio[company.name].amount))

        return PortfolioResponse(wallet_balance=user.balance, companies=result_companies)
