from pathlib import Path
import scrapinglab.extensions as extension_pkg

def test_extensions_package_has_init_file():
    assert hasattr(extension_pkg, '__file__'), (
        'extensions folder is missing an __init__.py'
        ' (treated as a namespace package)')
    init_path = Path(extension_pkg.__file__)
    assert init_path.is_file(), (
        f"Expected a file at {init_path}, but it does not exist.")
    assert init_path.name == '__init__.py', (
        f"Expected filename to be '__init__.py', got '{init_path.name}'")