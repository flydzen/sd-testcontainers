from client.actions.base_action import BaseAction


class WalletAction(BaseAction):
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def run(self) -> float:
        user = self.repository.get_user(self.user_id)
        return user.balance
