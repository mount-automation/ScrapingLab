from helper import (
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
    ids=provider.get_extension_module_ids(),)
def test_extensions_package_have_init_file(module_info):
    asserter.assert_subpackage_have_init(module_info=module_info)

@pytest.mark.parametrize(
    'loaded_module, loaded_module_main_cls',
    provider.get_extension_main_class(),
    ids=provider.get_extension_class_ids(),)
class TestExtensions:
    def test_extensions_have_url(
        self,
        loaded_module, 
        loaded_module_main_cls
    ):
        assert 'url' in loaded_module_main_cls.__dict__, (
            f'Variable url not found in: {
                loaded_module_main_cls.__module__}')
        assert validators.url(
            loaded_module_main_cls.__dict__['url']
            ) is True, (
            f'url string is not valid: {
                loaded_module_main_cls.__dict__["url"]
            }')

    # def test_extensions_have_run_method(self, module_info: ModuleInfo):
    #     module = importlib.import_module(module_info.name)
    #     classes = inspect.getmembers(module, inspect.isclass)
    #     for _, cls in classes:
    #         check = (
    #             cls.__module__.startswith(module.__name__)
    #             and
    #             cls is not BaseExtension
    #         )
    #         if check:
    #             assert 'run' in cls.__dict__, (
    #                 f'Object "run" not found in {cls.__module__}')
    #             assert callable(cls.__dict__['run']), (
    #                 f'Object "run" is not a function.')

    # def test_extension_inherit_from_base_extension(
    #     self, module_info: ModuleInfo):
    #     module = importlib.import_module(module_info.name)
    #     classes = inspect.getmembers(module, inspect.isclass)
    #     for _, cls in classes:
    #         check = (
    #             cls.__module__.startswith(module.__name__)
    #             and
    #             cls is not BaseExtension
    #         )
    #         if check:
    #             assert issubclass(cls, BaseExtension), (
    #                 f'Extension does not inherit from ' 
    #                 f'BaseExtension class: {cls.__module__}')