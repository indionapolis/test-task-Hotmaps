from unittest.mock import patch

import pytest

from src.datamodels import UserInfo
from src.service_client import ServiceClient, ServiceClientError
from tests.mocks import user_info_mock, auth_mock

SERVICE_URL = "http://testapi.ru/"


@pytest.fixture
def client():
    return ServiceClient(SERVICE_URL)


@pytest.fixture
def auth_client():
    client = ServiceClient(SERVICE_URL)
    client._token = "dsfd79843r32d1d3dx23d32d"
    return client


@pytest.mark.asyncio
@patch("src.service_client.ServiceClient._make_request")
async def test_service_auth(mock_response, client):
    mock_response.return_value = auth_mock

    await client.auth()


@pytest.mark.asyncio
@patch("src.service_client.ServiceClient._make_request")
async def test_get_user_info(mock_response, auth_client):
    mock_response.return_value = user_info_mock

    data = await auth_client.get_user_info("ivanov")

    assert data


@pytest.mark.asyncio
@patch("src.service_client.ServiceClient._make_request")
async def test_update_user_info(mock_response, auth_client):
    mock_response.return_value = user_info_mock

    await auth_client.update_user_info("0", UserInfo(**user_info_mock))


@pytest.mark.asyncio
@patch("src.service_client.ServiceClient._make_request")
async def test_get_user_info_not_auth(mock_response, client):
    mock_response.return_value = user_info_mock
    with pytest.raises(AssertionError):
        data = await client.get_user_info("ivanov")


@pytest.mark.asyncio
@patch("src.service_client.ServiceClient._make_request", autospec=True)
async def test_get_user_info_service_error(mock_response, auth_client):
    mock_response.side_effect = ServiceClientError()

    with pytest.raises(ServiceClientError):
        data = await auth_client.get_user_info("ivanov")
