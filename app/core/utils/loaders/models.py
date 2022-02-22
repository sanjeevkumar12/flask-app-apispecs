import importlib
import itertools
from inspect import getmembers, isclass
from os import listdir
from os import sep as pathsep
from os import walk
from os.path import isdir, join
from sys import modules

from flask_sqlalchemy import Model

from app.conf import BASE_DIR, MODEL_LOOKUP_EXCLUDE_DIRECTORY


def valid_module(path, module_name):
    if (
        isdir(join(path, module_name))
        and not module_name.startswith(".")
        and not module_name.startswith("__pycache")
        and module_name not in MODEL_LOOKUP_EXCLUDE_DIRECTORY
    ):
        return True
    return False


def list_dirs(path):
    return [d for d in listdir(path) if valid_module(path, d)]


def get_models():
    """Dynamic model finder."""

    all_dir = list_dirs(BASE_DIR)
    search_files = []
    for model_module in all_dir:
        for root, __, files in walk(join(BASE_DIR, model_module)):
            for filename in files:
                if filename.endswith(".py") and not filename.startswith("__init__"):
                    search_files.append(
                        ".".join(
                            [
                                root.split(str(BASE_DIR))[1]
                                .removeprefix(pathsep)
                                .replace(pathsep, "."),
                                filename[0:-3],
                            ]
                        )
                    )

    return list(
        itertools.chain(
            *[
                [
                    md[1]
                    for md in getmembers(importlib.import_module(file), is_model)
                    if md
                ]
                for file in search_files
            ]
        )
    )


def is_model(item):
    """Determines if `item` is a `db.Model`."""
    return isclass(item) and issubclass(item, Model)


def load_models():
    """Load application models for management script & app availability."""
    for model in get_models():
        setattr(modules[__name__], model.__name__, model)


__all__ = ("get_models", "load_models")
