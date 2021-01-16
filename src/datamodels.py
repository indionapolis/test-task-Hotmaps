from enum import Enum
from typing import List

from pydantic import BaseModel


class StatusEnum(str, Enum):
    ok = "OK"
    not_found = "NOT FOUND"
    error = "ERROR"


class ServiceResponse(BaseModel):
    status: StatusEnum


class Auth(ServiceResponse):
    token: str = None


class UserPermission(BaseModel):
    id: int
    permission: str


class UserInfo(BaseModel):
    active: str = None
    blocked: bool = None
    created_at: int = None
    id: int = None
    name: str = None
    permissions: List[UserPermission] = None


class UserInfoResponse(ServiceResponse, UserInfo):
    pass
