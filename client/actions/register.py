from client.actions.base_action import BaseAction


class RegisterAction(BaseAction):
    async def run(self) -> int:
        return self.repository.add_user()
