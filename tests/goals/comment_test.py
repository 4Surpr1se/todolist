import pytest

data = {
    'title': 'test_goal'
}


@pytest.mark.django_db
def test_goal(client, sessionid, goal_creater):
    client.cookies = sessionid
    data["goal"] = goal_creater
    response = client.post(path="/goals/goal_comment/create", data=data, content_type='application/json')

    assert response.status_code == 201, \
        'Ошибка при создании комментария при передаче валидных данных'


@pytest.mark.django_db
def test_comment_list(client, sessionid, board_creater):
    client.cookies = sessionid
    response = client.get(path="/goals/goal_comment/list", content_type='application/json')
    assert response.status_code == 200,\
        'Ошибка при выводе всех комментариев'
