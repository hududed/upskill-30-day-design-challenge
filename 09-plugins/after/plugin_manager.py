import importlib
import os
from decimal import Decimal
from importlib.util import module_from_spec, spec_from_file_location
from typing import Protocol


class Plugin(Protocol):
    @staticmethod
    def get_payment_method() -> str:
        ...
    @staticmethod
    def process_payment(total: Decimal) -> None:
        ...

PLUGINS: dict[str, Plugin] = {}

def import_module(name: str) -> Plugin:
    """ Imports a module given its name."""
    return importlib.import_module(name) # type: ignore

def load_plugins_from_folder(folder: str) -> None:
    """ Loads all modules from a folder."""
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                module_name = file[:-3]
                module_path = os.path.join(root, file)
                spec = spec_from_file_location(module_name, module_path)
                if spec:    
                    module: Plugin = module_from_spec(spec) # type: ignore
                    spec.loader.exec_module(module) # type: ignore
                    PLUGINS[module.get_payment_method()] = module

def get_plugin(name: str) -> Plugin:
    """ Returns a plugin given its name."""
    return PLUGINS[name]

def plugin_exists(name: str) -> bool:
    """ Returns True if a plugin exists, False otherwise."""
    return name in PLUGINS

def all_plugins() -> list[str]:
    """ Returns a list of all plugin names."""
    return list(PLUGINS.keys()) 
