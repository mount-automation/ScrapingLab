import pkgutil
import scrapinglab
import importlib.util
from pathlib import Path
from conftest import assert_subpackage_have_init

def test_package_has_init_file():
    scrapinglab_path_raw = scrapinglab.__path__
    assert len(scrapinglab_path_raw) == 1, (
        'There are possibilities of namespace '
        'package naming conflicts here.')
    scrapinglab_path = Path(scrapinglab_path_raw[0])
    for module_info in pkgutil.walk_packages(
        [scrapinglab_path], 'scrapinglab.'):
        assert_subpackage_have_init(module_info=module_info)