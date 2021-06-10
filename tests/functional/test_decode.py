from conftest import client


def make_encode_request(client):
    """
    Helper function to make the /encode request
    """
    return client.post(
        '/encode', json={'url': 'https://codesubmit.io/library/react'})


def make_decode_request(client, short_url):
    """
    Helper function to make the /decode request
    """
    return client.post(
        '/decode', json={'short_url': short_url})


def test_json_return(client):
    """
    GIVEN the /decode endpoint
    WHEN a valid request is made
    THEN check the response is JSON
    """

    encode_res = make_encode_request(client)
    encode_json = encode_res.get_json()
    short_url = encode_json['data']

    decode_res = make_decode_request(client, short_url=short_url)

    try:
        decode_res.get_json()
    except TypeError:
        assert False
    assert True


def test_response_structure(client):
    """
    GIVEN the /decode endpoint
    WHEN a valid request is made
    THEN check the response contains `message`
        and `data` keys
    """

    encode_res = make_encode_request(client)
    encode_json = encode_res.get_json()
    short_url = encode_json['data']

    decode_res = make_decode_request(client, short_url=short_url)

    json_data = decode_res.get_json()

    assert 'message' in json_data
    assert 'data' in json_data


def test_response_success(client):
    """
    GIVEN the /decode endpoint
    WHEN a valid request is made
    THEN check the value of `message` is success
    """

    encode_res = make_encode_request(client)
    encode_json = encode_res.get_json()
    short_url = encode_json['data']

    decode_res = make_decode_request(client, short_url=short_url)

    json_data = decode_res.get_json()

    assert json_data['message'] == 'success'


def test_decode_functionality(client):
    """
    GIVEN the /decode endpoint
    WHEN a valid request is made
    THEN check if the original URL returned in response
        matches the URL sent to /encode earlier
    """

    encode_res = make_encode_request(client)
    encode_json = encode_res.get_json()
    short_url = encode_json['data']

    decode_res = make_decode_request(client, short_url=short_url)

    json_data = decode_res.get_json()
    assert json_data['data'] == 'https://codesubmit.io/library/react'


def test_invalid_request(client):
    """
    GIVEN the /decode endpoint
    WHEN an invalid request is made
    THEN the response contains the `error` key and
        check the response code is 400
    """

    response = client.post('/decode', json={})
    json_data = response.get_json()
    assert 'errors' in json_data
    assert response.status_code == 400


def test_non_existent_url(client):
    """
    GIVEN the /decode endpoint
    WHEN a non-existent short URL is passed
    THEN the response contains the `error` key and
        check the response code is 404
    """

    response = client.post('/decode', json={'short_url': 'foobarqux'})
    json_data = response.get_json()
    assert 'errors' in json_data
    assert response.status_code == 404


def test_other_request_verbs_failing(client):
    """
    GIVEN the /decode endpoint
    WHEN invalid methods are requested
    THEN check the response code is 405
    """

    response = client.get('/decode', json={})
    assert response.status_code == 405
