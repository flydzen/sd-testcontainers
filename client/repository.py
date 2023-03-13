from dataclasses import dataclass, field, replace


@dataclass
class UserCompany:
    name: str
    amount: int


@dataclass
class User:
    id: int
    portfolio: dict[str, UserCompany] = field(default_factory=dict)
    balance: float = 0


class Repository:
    _instances = 0

    def __init__(self):
        Repository._instances += 1
        assert Repository._instances == 1

        self._user_num = 0
        self._users: dict[int, User] = {}

    def add_user(self) -> int:
        user_id = self._user_num
        self._user_num += 1
        self.save_user(User(user_id))
        return user_id

    def get_user(self, user_id) -> User | None:
        user = self._users.get(user_id)
        if user:
            user = replace(user)
        return user

    def save_user(self, user: User) -> None:
        self._users[user.id] = user

    def reset(self):
        self._user_num = 0
        self._users = {}