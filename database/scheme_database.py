from sqlmodel import SQLModel, Field
from typing import Optional


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    apartment_number: int
    owner: bool
    price: int
    creation_date: str
    nickname_telegram: str
    user_id_telega: int
    blocking: bool
    online_access: bool
    user_type: str
    date_issue: bool = True


class Dostup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    last_name: str
    number: str
    login: str
    password: str
    room: int
    access_transfer: bool = False
    date_access_transfer: str
    ip_address: str


class Video_request(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    room: int
    request_date: str
    time_range: str
    active: bool


class All_owners(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    l_name: str
    name: str
    f_name: str
    room: int
    number: str
