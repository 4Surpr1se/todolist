import pytest
data = {
        "username": "test_username_1",
        "old_password": "test_password",
        "new_password": "new_test_password"
    }


@pytest.mark.django_db
def test_reset_password(client, sessionid):
    client.cookies = sessionid
    response = client.put(path="/core/update_password", data=data, content_type='application/json')
    assert response.status_code == 200,\
        'Ошибка при смене пароля при передачи валидных данных'
    # assert str(response.data['password_repeat'][0]) == 'This field is required.'
    # assert str(response.data['username'][0]) == 'A user with that username already exists.'
    # assert str(response.data['email'][0]) == 'Enter a valid email address.'


@pytest.mark.django_db
def test_reset_wrong_password(client, sessionid):
    validators_list = ['This password is too short. It must contain at least 7 characters.',
                       'This password is too common.',
                       'This password is entirely numeric.']
    client.cookies = sessionid
    data["new_password"] = "1234"
    response = client.put(path="/core/update_password", data=data, content_type='application/json')
    assert list(map(str, response.data['new_password'])) == validators_list,\
        'Неверно совершена проверка пароля'


@pytest.mark.django_db
def test_reset_password_missing(client, sessionid):
    client.cookies = sessionid
    data.pop("new_password")
    response = client.put(path="/core/update_password", data=data, content_type='application/json')
    assert response.data['new_password'][0] == 'This field is required.',\
        'Нет проверки на передачу пользователем поля new_password'

