import inspect
import importlib
import pkgutil
from pkgutil import ModuleInfo
from pathlib import Path
import scrapinglab.extensions as extensions
from scrapinglab.extensions import BaseExtension
from types import ModuleType

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

def get_extension_module_ids():
    module_info_list: list[ModuleInfo] = get_all_extensions()
    formatted_ids = []
    for module_info in module_info_list:
        formatted_ids.append(module_info.name)
    return formatted_ids

def get_extension_main_class():
    module_info: ModuleInfo
    extension_main_class_list = []
    for module_info in get_all_extensions():
        loaded_module = importlib.import_module(module_info.name)
        loaded_module_cls_list = inspect.getmembers(
            loaded_module, inspect.isclass)
        for _, cls in loaded_module_cls_list:
            if is_local_main_class(cls=cls, module=loaded_module):
                extension_main_class_list.append((loaded_module, cls))
    return extension_main_class_list

def get_extension_class_ids():
    module: ModuleType
    cls: type
    extension_class_ids = []
    for module, cls in get_extension_main_class():
        extension_class_ids.append(f'{module.__name__}.{cls.__name__}')
    return extension_class_ids

def is_local_main_class(cls: type, module: ModuleType):
    return (
        cls.__module__.startswith(module.__name__)
        and
        cls is not BaseExtension
    )