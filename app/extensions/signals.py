from typing import Callable

from blinker import NamedSignal
from flask import Flask
from flask.signals import Namespace, _signals


def init_signal(app: Flask):
    pass


def register_signal(label: str, callable_func: Callable) -> NamedSignal:
    function = _signals.signal(label)
    function.connect(callable_func)
    return function
