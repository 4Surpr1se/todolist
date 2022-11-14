from http.cookies import SimpleCookie

import pytest

data = {
    'title': 'test_category'
}


@pytest.mark.django_db
def test_category(client, board_creater, sessionid):
    client.cookies = sessionid
    data["board"] = board_creater
    response = client.post(path="/goals/goal_category/create", data=data, content_type='application/json')
    assert response.status_code == 201, \
        'Ошибка при создании категории при передаче валидных данных'


@pytest.mark.django_db
def test_category_missing_field(client, sessionid):
    client.cookies = sessionid
    data.pop("board")
    response = client.post(path="/goals/goal_category/create", data=data, content_type='application/json')
    assert response.data['board'][0] == 'This field is required.', \
        'Нет проверки на передачу пользователем поля board'


@pytest.mark.django_db
def test_category_list(client, sessionid, board_creater):
    client.cookies = sessionid
    response = client.get(path="/goals/goal_category/list", content_type='application/json')
    assert response.status_code == 200, \
        'Ошибка при выводе всех категорий'
