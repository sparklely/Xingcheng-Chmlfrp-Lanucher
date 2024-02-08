'''
from typing import TypeAlias

JSON: TypeAlias = dict
'''

class User:
    id: int = None
    token: str = None
    TunList: list = []
    TunDict: dict = {}
    TunData: list = None
    LoginData: dict = None

class GUI:
    tkObj=None