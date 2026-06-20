import inspect
import importlib
import pkgutil
from pkgutil import ModuleInfo
from pathlib import Path
import scrapinglab.extensions as extensions
from scrapinglab.extensions import BaseExtension

def get_all_extensions():
    assert len(extensions.__path__) == 1, (
        'There are possibilities of namespace '
        'package naming conflicts here.')
    extensions_path = Path(extensions.__path__[0])
    module_info_list = []
    for module_info in pkgutil.iter_modules(
        [extensions_path],
        'scrapinglab.extensions.'):
        module_info_list.append(module_info)
    return module_info_list

def get_formatted_ids():
    module_info_list: list[ModuleInfo] = get_all_extensions()
    formatted_ids = []
    for module_info in module_info_list:
        formatted_ids.append(module_info.name)
    return formatted_ids

from types import ModuleType
LOADED_MODULE_CLASSES = list[tuple[str, type]]
LOADED_EXTENSION_ARTIFACTS = tuple[ModuleType, LOADED_MODULE_CLASSES]
def get_extension_classes(
    module_info: ModuleInfo
) -> LOADED_EXTENSION_ARTIFACTS:
    module: ModuleType = importlib.import_module(module_info.name)
    classes: LOADED_MODULE_CLASSES = inspect.getmembers(
        module, inspect.isclass)
    return module, classes

def check_loaded_module_main_class(cls: type, loaded_module: ModuleType):
    return (
        cls.__module__.startswith(loaded_module.__name__) 
        and
        cls is not BaseExtension
    )