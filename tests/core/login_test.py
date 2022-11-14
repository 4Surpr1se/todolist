from http.cookies import Morsel, SimpleCookie

import pytest
from django.http import HttpRequest, JsonResponse

data = {
        "username": "test_username_1",
        "password": "test_password",
        "password_repeat": "test_password"
    }


@pytest.mark.django_db
def test_cookie_set(client, signingup):
    response = client.post(path="/core/login", data=data)

    assert response.cookies["sessionid"].coded_value,\
            'Ползьователю не передается в куки аутентефекатор сессии'
    assert response.status_code == 200,\
        'Ошибка в логировании при передаче валидных данных'



@pytest.mark.django_db
def test_logout(client, signingup):
    response = client.post(path="/core/login", data=data)
    client.cookies = SimpleCookie({'sessionid': response.cookies["sessionid"]})
    response1 = client.delete(path="/core/login", data=data)

    assert response1.status_code == 200,\
            'Ошибка в logout при передаче валидных данных'
