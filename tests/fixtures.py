from http.cookies import SimpleCookie

import pytest

from tests.core.login_test import data
from tests.goals.board_test import data as data_board
from tests.goals.goalcategory_test import data as data_category
from tests.goals.goals_test import data as data_goals


@pytest.fixture
@pytest.mark.django_db
def signingup(client):
    client.post(path="/core/signup", data=data)


@pytest.fixture
@pytest.mark.django_db
def sessionid(client):
    client.post(path="/core/signup", data=data)
    response = client.post(path="/core/login", data=data)
    return SimpleCookie({'sessionid': response.cookies["sessionid"]})


@pytest.fixture
@pytest.mark.django_db
def board_creater(client):
    client.post(path="/core/signup", data=data)

    response = client.post(path="/core/login", data=data)
    client.cookies = SimpleCookie({'sessionid': response.cookies["sessionid"]})

    response = client.post(path="/goals/board/create", data=data_board,
                           content_type='application/json')
    return response.data["id"]


@pytest.fixture
@pytest.mark.django_db
def category_creater(client):
    client.post(path="/core/signup", data=data)

    response = client.post(path="/core/login", data=data)
    client.cookies = SimpleCookie({'sessionid': response.cookies["sessionid"]})

    response = client.post(path="/goals/board/create", data=data_board,
                           content_type='application/json')

    data_category["board"] = response.data["id"]
    response = client.post(path="/goals/goal_category/create", data=data_category,
                           content_type='application/json')

    return response.data["id"]


@pytest.fixture
@pytest.mark.django_db
def goal_creater(client):
    client.post(path="/core/signup", data=data)

    response = client.post(path="/core/login", data=data)
    client.cookies = SimpleCookie({'sessionid': response.cookies["sessionid"]})

    response = client.post(path="/goals/board/create", data=data_board,
                           content_type='application/json')

    data_category["board"] = response.data["id"]
    response = client.post(path="/goals/goal_category/create", data=data_category,
                           content_type='application/json')

    data_goals["category"] = response.data["id"]
    response = client.post(path="/goals/goal/create", data=data_goals,
                           content_type='application/json')

    return response.data["id"]
