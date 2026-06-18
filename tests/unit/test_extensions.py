import validators
import pkgutil
from pkgutil import (
    ModuleInfo,
)
import inspect
import pytest
import importlib
import importlib.util
import scrapinglab.extensions as extensions
from pathlib import Path
from conftest import assert_subpackage_have_init
from scrapinglab.extensions.core import BaseExtension
from urllib.parse import urlparse

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

@pytest.mark.parametrize(
    'module_info',
    get_all_extensions(),
    ids=get_formatted_ids(),)
class TestExtensions:
    def test_extensions_package_have_init_file(self, module_info):
        assert_subpackage_have_init(module_info=module_info)

    def test_extensions_have_url(self, module_info: ModuleInfo):
        module = importlib.import_module(module_info.name)
        classes = inspect.getmembers(module, inspect.isclass)
        for _, cls in classes:
            check = (
                cls.__module__.startswith(module.__name__) 
                and
                cls is not BaseExtension
            )
            if check:
                assert 'url' in cls.__dict__, (
                    f'Variable url not found in: {cls.__module__}')
                assert validators.url(cls.__dict__['url']) is True, (
                    f'url string is not valid: {cls.__dict__['url']}')

    def test_extensions_have_run_method(self, module_info: ModuleInfo):
        module = importlib.import_module(module_info.name)
        classes = inspect.getmembers(module, inspect.isclass)
        for _, cls in classes:
            check = (
                cls.__module__.startswith(module.__name__)
                and
                cls is not BaseExtension
            )
            if check:
                assert 'run' in cls.__dict__, (
                    f'Object "run" not found in {cls.__module__}')
                assert callable(cls.__dict__['run']), (
                    f'Object "run" is not a function.')

    def test_extension_inherit_from_base_extension(
        self, module_info: ModuleInfo):
        module = importlib.import_module(module_info.name)
        classes = inspect.getmembers(module, inspect.isclass)
        for _, cls in classes:
            check = (
                cls.__module__.startswith(module.__name__)
                and
                cls is not BaseExtension
            )
            if check:
                assert issubclass(cls, BaseExtension), (
                    f'Extension does not inherit from ' 
                    f'BaseExtension class: {cls.__module__}')