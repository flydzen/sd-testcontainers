from abc import ABC, abstractmethod

from stock.repository import StockRepository


class BaseAction(ABC):
    repository: StockRepository

    @abstractmethod
    def run(self):
        pass

