import pytest
from starlette.testclient import TestClient

from base.base import Company
from stock.main import app, repository
from hamcrest import not_none, assert_that, has_entries


@pytest.fixture
def client():
    return TestClient(app)


def test_full_info_empty(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == []


def test_create_company(client):
    response = client.post('/company?name=test&price=10&amount=1')
    assert response.status_code == 200
    assert len(repository._companies) == 1
    assert repository._companies == {'test': Company(name='test', price=10, amount=1)}


def test_get_company(client):
    assert client.post('/company?name=test&price=10').status_code == 200
    response = client.get('/company?name=test')

    assert response.status_code == 200

    assert_that(
        response.json(),
        has_entries(name='test', price=not_none(), amount=0),
    )


def test_fill_company(client):
    assert client.post('/company?name=test&price=10&amount=0').status_code == 200
    assert client.post('/fill?name=test&amount=200').status_code == 200

    response = client.get('/company?name=test')

    assert response.status_code == 200

    assert_that(
        response.json(),
        has_entries(name='test', price=not_none(), amount=200),
    )


def test_buy(client):
    assert client.post('/company?name=test&price=100&amount=200').status_code == 200
    r1 = client.post('/buy?name=test&amount=100')
    assert r1.status_code == 200
    assert 100 * 100 / 2 < r1.json()['expenditure'] < 100 * 100 * 2

    response = client.get('/company?name=test')

    assert response.status_code == 200

    assert_that(
        response.json(),
        has_entries(name='test', price=not_none(), amount=100),
    )


def test_sell(client):
    assert client.post('/company?name=test&price=100&amount=200').status_code == 200
    r1 = client.post('/sell?name=test&amount=100')
    assert r1.status_code == 200
    assert 100 * 100 / 2 < r1.json()['revenue'] < 100 * 100 * 2

    response = client.get('/company?name=test')
    assert response.status_code == 200

    assert_that(
        response.json(),
        has_entries(name='test', price=not_none(), amount=300),
    )
