import time

import pytest
import requests
from starlette.testclient import TestClient
from testcontainers.core.container import DockerContainer

from client.main import app


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

# docker build -t stock .
# docker run -it -d --name stock_container -p 8081:8081 stock
