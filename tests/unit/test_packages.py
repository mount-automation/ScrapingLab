import pkgutil
import scrapinglab
import importlib.util
from pathlib import Path

def test_package_has_init_file():
    scrapinglab_path_raw = scrapinglab.__path__
    assert len(scrapinglab_path_raw) == 1, (
        'There are possibilities of namespace '
        'package naming conflicts here.')
    scrapinglab_path = Path(scrapinglab_path_raw[0])
    for module_info in pkgutil.walk_packages(
        [scrapinglab_path], 'scrapinglab.'):
        if module_info.ispkg:
            module_spec = importlib.util.find_spec(module_info.name)
            assert module_spec, (
                f'Module specifications could not be retrieved.')
            assert module_spec.origin, (
                f'Module specification path could not be retrieved. '
                f'This might due to this package not having an '
                f'__init__.py file. Package in question is: '
                f'{module_info.name}')
            package_path = Path(module_spec.origin)
            assert '__init__' in module_spec.origin, (
                f'The following package has no __init__.py file: '
                f'{package_path.stem}')