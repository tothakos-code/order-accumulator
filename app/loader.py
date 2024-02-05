import importlib
import logging
from app.vendor_factory import VendorFactory
from app.base_vendor import BaseVendor

class ModuleInterface:

    @staticmethod
    def register() -> None:
        pass

def import_module(name: str) -> ModuleInterface:
    """Imports a module given a name."""
    return importlib.import_module(name)  # type: ignore


def load_plugins(plugins: list) -> None:
    """Loads the plugins defined in the plugins list."""
    for plugin_file in plugins:
        plugin = import_module(plugin_file+".app")

        logging.info("Loaded {0} plugin".format(plugin.__name__))

        for name, obj in plugin.__dict__.items():
            if isinstance(obj, type) and issubclass(obj, BaseVendor) and obj != BaseVendor:
                VendorFactory.register(obj())