'''
from typing import TypeAlias

JSON: TypeAlias = dict
'''

class User:
    id: int = None
    token: str = None
    TunList: list = None
    TunDict: dict = None
    LoginData: dict = None

class GUI:
    tkObj=None