from http.cookies import SimpleCookie

import pytest

data = {
    'title': 'test_board'
}


@pytest.mark.django_db
def test_board(client, sessionid):
    client.cookies = sessionid
    response = client.post(path="/goals/board/create", data=data, content_type='application/json')
    assert response.status_code == 201, \
        'Ошибка при создании доски при передаче валидных данных'


@pytest.mark.django_db
def test_board_missing_field(client, sessionid):
    client.cookies = sessionid
    data.pop('title')
    response = client.post(path="/goals/board/create", data=data, content_type='application/json')
    assert response.data['title'][0] == 'This field is required.', \
        'Нет проверки на передачу пользователем поля title'


@pytest.mark.django_db
def test_board_list(client, sessionid):
    client.cookies = sessionid
    response = client.get(path="/goals/board/list", content_type='application/json')
    assert response.status_code == 200, \
        'Ошибка при выводе всех досок'
