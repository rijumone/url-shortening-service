from conftest import client


def make_request(client):
    """
    Helper function to make the /encode request
    """
    return client.post(
        '/encode', json={'url': 'https://codesubmit.io/library/react'})


def test_json_return(client):
    """
    GIVEN the /encode endpoint
    WHEN a valid request is made
    THEN check the response is JSON
    """

    response = make_request(client)
    try:
        response.get_json()
    except TypeError:
        assert False
    assert response.status_code == 200


def test_len_shorturl(client):
    """
    GIVEN the /encode endpoint
    WHEN a valid request is made
    THEN check the shortened url contains the hash
        exactly 5 characters long
    """

    response = make_request(client)

    json_data = response.get_json()
    short_url_suffix = json_data['data'].split('/')[-1]
    assert len(short_url_suffix) == 5


def test_response_structure(client):
    """
    GIVEN the /encode endpoint
    WHEN a valid request is made
    THEN check the response contains `message`
        and `data` keys
    """

    response = make_request(client)

    json_data = response.get_json()

    assert 'message' in json_data
    assert 'data' in json_data


def test_response_success(client):
    """
    GIVEN the /encode endpoint
    WHEN a valid request is made
    THEN check the value of `message` is success
    """

    response = make_request(client)

    json_data = response.get_json()

    assert json_data['message'] == 'success'


def test_other_request_method_failing(client):
    """
    GIVEN the /encode endpoint
    WHEN invalid methods are requested
    THEN check the response code is 405
    """

    response = client.get('/encode', json={})
    assert response.status_code == 405


def test_invalid_request(client):
    """
    GIVEN the /encode endpoint
    WHEN an invalid request is made
    THEN the response contains the `error` key and
        check the response code is 400
    """

    response = client.post(
        '/encode', json={'url1': 'https://codesubmit.io/library/react'})
    json_data = response.get_json()
    assert 'errors' in json_data
    assert response.status_code == 400
