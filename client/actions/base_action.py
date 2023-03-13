from abc import ABC, abstractmethod

from client.repository import Repository


class BaseAction(ABC):
    repository: Repository

    @abstractmethod
    async def run(self):
        pass

