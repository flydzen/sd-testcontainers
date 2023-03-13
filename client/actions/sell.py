from base.exceptions import NotEnoughSharesError
from client.actions.base_action import BaseAction
from client.interaction import Interaction


class SellAction(BaseAction):
    def __init__(self, user_id: int, company_name: str, amount: int):
        self.user_id = user_id
        self.company_name = company_name
        self.amount = amount

    async def run(self) -> float:
        user = self.repository.get_user(self.user_id)
        company = await Interaction.get_company(self.company_name)
        if user.balance is None:
            raise
        if user.balance < self.amount * company.price:
            raise NotEnoughSharesError
        revenue = await Interaction.sell(self.company_name, self.amount)
        user.balance += revenue
        self.repository.save_user(user)
        return revenue
