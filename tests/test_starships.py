# import pytest
# from flask import url_for


def test_list_starships(client):
    """Should return a list of starships."""

    resp = client.get('/api/starships/')

    assert resp.status_code == 200
