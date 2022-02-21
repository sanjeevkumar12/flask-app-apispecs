import importlib


def load_module(module_class: str):
    module_name, class_name = module_class.rsplit(".", 1)
    module = importlib.import_module(module_name)
    assert hasattr(module, class_name), "class {} is not in {}".format(
        class_name, module_name
    )
    return getattr(module, class_name)
