from dataclasses import replace
from datetime import datetime
import random
from math import sqrt

from base.base import Company


class StockRepository:
    _instances = 0
    SIGMA = 0.1

    def __init__(self):
        StockRepository._instances += 1
        assert StockRepository._instances == 1

        self._last_update = datetime.now()
        self._companies: dict[str, Company] = {}
        random.seed(self._last_update)

    def set_company(self, company: Company) -> None:
        self._companies[company.name] = company

    def get_company(self, name: str) -> Company | None:
        self._update()
        company = self._companies.get(name)
        if company:
            company = replace(company)
        return company

    def get_companies(self) -> list[Company]:
        self._update()
        return list(map(replace, self._companies.values()))

    def _update(self) -> None:
        offset = (datetime.now() - self._last_update).total_seconds()
        sigma = sqrt(StockRepository.SIGMA ** 2 * offset)

        for company in self._companies.values():
            change = random.gauss(0, sigma)
            company.price += change
