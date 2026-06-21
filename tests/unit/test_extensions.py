from helper import (
    asserter,
    provider,)
import pytest
import validators
from scrapinglab.extensions.core import BaseExtension
from helper.provider import LoadedExtensionMainClassCase

@pytest.mark.parametrize(
    'module_info',
    provider.get_all_extensions(),
    ids=provider.get_extension_module_ids(),)
def test_extensions_package_have_init_file(module_info):
    asserter.assert_subpackage_have_init(module_info=module_info)

@pytest.mark.parametrize(
    'case',
    provider.get_extension_main_class(),
    ids=provider.get_extension_class_ids(),)
class TestExtensions:
    def test_extensions_have_url(
        self,
        case: LoadedExtensionMainClassCase,
    ):
        assert 'url' in case.cls.__dict__, (f'Variable url not found in: '
            f'{case.cls.__module__}'
        )
        assert validators.url(case.cls.__dict__['url']) is True, (
            f'url string is not valid: {case.cls.__dict__["url"]}')

    def test_extensions_have_run_method(
        self,
        case: LoadedExtensionMainClassCase,
    ):
        assert 'run' in case.cls.__dict__, (
            f'Object "run" not found in '
            f'{case.cls.__module__}')
        assert callable(case.cls.__dict__['run']), (
            f'Object "run" is not a function.')

    def test_extension_inherit_from_base_extension(
        self, 
        case: LoadedExtensionMainClassCase,
    ):
        assert issubclass(case.cls, BaseExtension), (
            f'Extension does not inherit from ' 
            f'BaseExtension class: {case.cls.__module__}')