from client.actions.base_action import BaseAction


class FillAction(BaseAction):
    def __init__(self, user_id: int, amount: float):
        self.user_id = user_id
        self.amount = amount

    async def run(self) -> None:
        user = self.repository.get_user(self.user_id)
        user.balance += self.amount
        self.repository.save_user(user)
