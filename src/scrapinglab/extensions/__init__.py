from .core import BaseExtension
from .split_testing import SplitTesting
from .add_remove_elements import AddRemoveElements
from .basic_auth import BasicAuth
from .broken_images import BrokenImages
from .challenging_dom import ChallengingDOM
from .checkboxes import CheckBoxes
from .context_menu import ContextMenu
from .digest_auth import DigestAuth
from .disappearing_elements import DisappearingElements
from .drag_and_drop import DragAndDrop

ACTIVE_EXTENSIONS: list[type[BaseExtension]] = [
    # SplitTesting,
    # AddRemoveElements,
    # BasicAuth,
    # BrokenImages,
    # ChallengingDOM,
    # CheckBoxes,
    # ContextMenu,
    # DigestAuth,
    # DisappearingElements,
    DragAndDrop,
]