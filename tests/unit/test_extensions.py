from .helper import (
    asserter,
    provider,)
import pytest
from pkgutil import ModuleInfo
import inspect
import importlib
import validators
from pathlib import Path
import scrapinglab.extensions as extensions
from scrapinglab.extensions.core import BaseExtension
from urllib.parse import urlparse

@pytest.mark.parametrize(
    'module_info',
    provider.get_all_extensions(),
    ids=provider.get_formatted_ids(),)
class TestExtensions:
    def test_extensions_package_have_init_file(self, module_info):
        asserter.assert_subpackage_have_init(module_info=module_info)

    def test_extensions_have_url(self, module_info: ModuleInfo):
        result = provider.get_extension_classes(module_info)
        loaded_module, loaded_module_cls_list = result
        for _, cls in loaded_module_cls_list:
            result = provider.check_loaded_module_main_class(
                cls=cls, loaded_module=loaded_module)
            if result:
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