from client.actions.base_action import BaseAction
from client.interaction import Interaction


class BalanceAction(BaseAction):
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def run(self) -> float:
        user = self.repository.get_user(self.user_id)
        companies = await Interaction.get_companies()
        summ = user.balance
        for company in companies:
            if company.name in user.portfolio:
                summ += user.portfolio[company.name].amount * company.price

        return summ
