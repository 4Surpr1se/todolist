

import pytest

data = {
    'title': 'test_goal',
    'description': 'test_description'
}


@pytest.mark.django_db
def test_goal(client, sessionid, category_creater):
    client.cookies = sessionid
    data["category"] = category_creater
    response = client.post(path="/goals/goal/create", data=data, content_type='application/json')
    assert response.status_code == 201, \
        'Ошибка при создании цели при передаче валидных данных'


@pytest.mark.django_db
def test_goal_missing_field(client, sessionid):
    client.cookies = sessionid
    data.pop("category")
    response = client.post(path="/goals/goal/create", data=data, content_type='application/json')
    assert response.data['category'][0] == 'This field is required.', \
        'Нет проверки на передачу пользователем поля category'


@pytest.mark.django_db
def test_goal_list(client, sessionid, board_creater):
    client.cookies = sessionid
    response = client.get(path="/goals/goal/list", content_type='application/json')
    assert response.status_code == 200, \
        'Ошибка при выводе всех целей'
