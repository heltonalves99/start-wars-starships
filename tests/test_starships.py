import requests

from werkzeug.exceptions import NotFound, ServiceUnavailable
from unittest.mock import patch
from unittest import mock

from mock_data import (mock_starships_page_1,
                       mock_starships_page_2,
                       mock_empty_starships,
                       mock_empty_unknown_hyperdrive)


class MockResponse:
    def __init__(self, mock_starships):
        self.mock_starships = mock_starships

    def json(self):
        return self.mock_starships

    def raise_for_status(self):
        pass


class MockBadResponse:
    def __init__(self, exceptions, description="Page not found"):
        self.exceptions = exceptions
        self.description = description

    def raise_for_status(self):
        raise self.exceptions(self.description)


def test_list_starships(client):
    """Should return a list of starships."""

    with patch("requests.get", return_value=MockResponse(mock_starships_page_1)):
        resp = client.get("/api/starships/")

        assert resp.status_code == 200
        assert len(resp.json["starships"]) == 2
        assert len(resp.json["starships_unknown_hyperdrive"]) == 1

        assert resp.json["starships"][0]["name"] == "Sentinel-class landing craft"
        assert resp.json["starships_unknown_hyperdrive"][0]["name"] == "EF76 Nebulon-B escort frigate"


def test_empty_starships(client):
    """Should return a empty list of starships."""

    with patch("requests.get", return_value=MockResponse(mock_empty_starships)):
        resp = client.get("/api/starships/")

        assert resp.status_code == 200
        assert len(resp.json["starships"]) == 0
        assert len(resp.json["starships_unknown_hyperdrive"]) == 1


def test_empty_starships_unknown_hyperdrive(client):
    """Should return a empty list of starships_unknown_hyperdrive."""

    with patch("requests.get", return_value=MockResponse(mock_empty_unknown_hyperdrive)):
        resp = client.get("/api/starships/")

        assert resp.status_code == 200
        assert len(resp.json["starships_unknown_hyperdrive"]) == 0
        assert len(resp.json["starships"]) == 2

    
def test_list_starships_with_next_page(client):
    """Should exist next page."""

    with patch("requests.get", return_value=MockResponse(mock_starships_page_1)):
        resp = client.get("/api/starships/")

        assert resp.json["next"].endswith("/api/starships/?page=2")


def test_list_starships_without_next_page(client):
    """Should not exist next page."""

    with patch("requests.get", return_value=MockResponse(mock_starships_page_2)):
        resp = client.get("/api/starships/?page=2")

        assert resp.status_code == 200
        assert resp.json["next"] is None


def test_list_starships_with_prev_page(client):
    """Should exist prev page."""

    with patch("requests.get", return_value=MockResponse(mock_starships_page_2)):
        resp = client.get("/api/starships/?page=2")

        assert resp.json["prev"].endswith("/api/starships/?page=1")


def test_list_starships_without_prev_page(client):
    """Should exist next page."""

    with patch("requests.get", return_value=MockResponse(mock_starships_page_1)):
        resp = client.get("/api/starships/")

        assert resp.json["prev"] is None


def test_list_starships_pagination_page_404(client):
    """Should status code 404 if page range not exists."""

    with patch("requests.get", return_value=MockBadResponse(NotFound)):
        resp = client.get("/api/starships/?page=80")

        assert resp.status_code == 404
