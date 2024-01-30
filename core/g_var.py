from typing import TypeAlias

JSON: TypeAlias = dict

class User:
    id: int = None
    token: str = None
    LoginData: JSON = None