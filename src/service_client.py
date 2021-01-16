from urllib.parse import urljoin

import aiohttp

from src.datamodels import Auth, UserInfo, UserInfoResponse


class ServiceClientError(Exception):
    """
    This error generated whenever outgoing or ingoing data dose not
    correspond to expected schemas or when external service is out of service
    """


class ServiceClient:
    def __init__(self, url, login="test", password="12345"):
        self._url = url
        self._login = login
        self._password = password

        self._token = None

    async def auth(self):
        params = {"login": self._login, "password": self._password}

        response = await self._make_request("GET", "auth", params=params)
        auth_response = Auth(**response)

        self._token = auth_response.token

    async def get_user_info(self, username: str) -> UserInfoResponse:
        assert self._token, "service token is not set, call .auth() first"
        params = {"token": self._token}

        response = await self._make_request(
            "GET", f"get-user/{username}", params=params
        )
        user_info_response = UserInfoResponse(**response)

        return user_info_response

    async def update_user_info(self, user_id: str, user_info: UserInfo):
        assert self._token, "service token is not set, call .auth() first"
        params = {"token": self._token}
        body = user_info.dict()

        response = await self._make_request(
            "POST", f"user/{user_id}/update", params=params, json=body
        )

    async def _make_request(self, method, endpoint, **kwargs) -> dict:
        request_url = urljoin(self._url, endpoint)

        async with aiohttp.ClientSession() as session:
            async with session.request(method, request_url, **kwargs) as response:
                if response.ok:
                    return await response.json()
                else:
                    raise ServiceClientError(response.status)
