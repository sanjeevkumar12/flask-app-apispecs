from typing import TypedDict, Any


class Route(TypedDict):
    path: str
    view_func: Any
