from flask.signals import Namespace
from flask.signals import _signals
from blinker import NamedSignal
from typing import Callable
from flask import Flask


def init_signal(app: Flask):
    pass

def register_signal(label: str, callable_func: Callable) -> NamedSignal:
    function = _signals.signal(label)
    function.connect(callable_func)
    return function
