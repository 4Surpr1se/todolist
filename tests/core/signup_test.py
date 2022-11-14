import pytest


data = {
        "username": "test_username_2",
        "password": "test_password",
        "password_repeat": "test_password",
        "first_name": "test_first_name",
        "last_name": "test_last_name"
    }


@pytest.mark.django_db
def test_signup_status(client):
    response = client.post(path="/core/signup", data=data)
    assert response.status_code == 201,\
        'Ошибка при регистрации при передачи валидных данных'


@pytest.mark.django_db
def test_signup_pass_hash(client):
    response = client.post(path="/core/signup", data=data)

    assert response.data["password"][:14] == "pbkdf2_sha256$",\
        'Пользователю не передается хэш от пароля или хэширование не через pbkdf2_sha256'


@pytest.mark.django_db
def test_signup_fields_check(user, client):
    data.pop("password_repeat")
    data["username"] = "test_username"
    data["email"] = 'aasd'
    response = client.post(path="/core/signup", data=data)

    assert str(response.data['password_repeat'][0]) == 'This field is required.',\
        'Нет проверки на передачу пользователем поля password_repeat'

    assert str(response.data['username'][0]) == 'A user with that username already exists.',\
        'Нет проверки на передачу пользователем поля username'

    assert str(response.data['email'][0]) == 'Enter a valid email address.',\
        'Нет валидатора поля email или сведения о не валидности не передаются пользователю'
