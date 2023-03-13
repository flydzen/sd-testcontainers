import time

import pytest
import requests
from starlette.testclient import TestClient
from testcontainers.core.container import DockerContainer
from hamcrest import close_to, assert_that

from client.main import app, repository


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def stock():
    with DockerContainer('stock').with_bind_ports(8081, 8081) as container:
        time.sleep(1)
        yield container


def test_welcome(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.text == 'Добро пожаловать на биржу!'


def test_register(client):
    response = client.post('/register')
    assert response.status_code == 200
    assert response.json() == {'user_id': 0}


def test_wallet(client):
    assert client.post('/register').status_code == 200

    response = client.get('/0/wallet')
    assert response.status_code == 200
    assert response.json() == {'wallet': 0}


def test_fill(client):
    assert client.post('/register').status_code == 200

    assert client.post('/0/fill?money_amount=200').status_code == 200

    response = client.get('/0/wallet')
    assert response.status_code == 200
    assert response.json() == {'wallet': 200}


def test_stock(stock):
    x = requests.get('http://localhost:8081/', timeout=10)
    assert x.status_code == 200


def test_buy(client, stock):
    repository.reset()
    assert requests.post('http://localhost:8081/company?name=test&price=10&amount=200', timeout=10).status_code == 200
    assert client.post('/register').status_code == 200
    assert client.post('/0/fill?money_amount=20000').status_code == 200

    request = client.post('/0/buy?company_name=test&amount=199')
    assert request.status_code == 200
    expenditure = request.json()['expenditure']
    assert 200 * 10 / 2 < expenditure < 200 * 10 * 2

    assert client.get('/0/wallet').json() == {'wallet': 20000 - expenditure}


def test_sell(client, stock):
    repository.reset()
    assert requests.post('http://localhost:8081/company?name=test&price=10&amount=200', timeout=10).status_code == 200
    assert client.post('/register').status_code == 200
    assert client.post('/0/fill?money_amount=20000').status_code == 200

    assert client.post('/0/buy?company_name=test&amount=199').status_code == 200

    wallet1 = client.get('/0/wallet').json()['wallet']
    response = client.post('/0/sell?company_name=test&amount=199')
    assert response.status_code == 200
    assert 'revenue' in response.json()

    wallet2 = client.get('/0/wallet').json()['wallet']
    assert wallet2 + response.json()['revenue'] + wallet1


def test_portfolio(client, stock):
    repository.reset()
    assert requests.post('http://localhost:8081/company?name=test1&price=5&amount=20', timeout=10).status_code == 200
    assert requests.post('http://localhost:8081/company?name=test2&price=8&amount=20', timeout=10).status_code == 200

    assert client.post('/register').status_code == 200
    assert client.post('/0/fill?money_amount=22000').status_code == 200
    response1 = client.post('/0/buy?company_name=test1&amount=2')
    response2 = client.post('/0/buy?company_name=test2&amount=4')
    assert response1.status_code == 200
    assert response2.status_code == 200

    spend = response1.json()['expenditure'] + response2.json()['expenditure']

    r_portfolio = client.get('/0/portfolio')
    assert r_portfolio.status_code == 200
    portfolio = r_portfolio.json()
    assert_that(portfolio['wallet_balance'], close_to(22000 - spend, 1))
    assert len(portfolio['companies']) == 2
    assert sum(map(lambda x: x['amount'], portfolio['companies'])) == 6


def test_total_balance(client, stock):
    repository.reset()
    assert requests.post('http://localhost:8081/company?name=test1&price=10&amount=200', timeout=10).status_code == 200
    assert requests.post('http://localhost:8081/company?name=test2&price=10&amount=200', timeout=10).status_code == 200
    assert client.post('/register').status_code == 200
    assert client.post('/0/fill?money_amount=2200').status_code == 200

    assert client.post('/0/buy?company_name=test1&amount=5').status_code == 200
    assert client.post('/0/buy?company_name=test2&amount=10').status_code == 200

    balance = client.get('/0/balance')
    assert balance.status_code == 200
    assert_that(balance.json()['total_wallet'], close_to(2200, 1))

# docker build -t stock .
# docker run -it -d --name stock_container -p 8081:8081 stock
