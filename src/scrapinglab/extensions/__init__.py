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
from .dropdown import Dropdown
from .dynamic_content import DynamicContent
from .dynamic_controls import DynamicControls
from .dynamic_loading import DynamicLoading
from .entry_ad import EntryAd
from .exit_intent import ExitIntent
from .file_downloader import FileDownloader
from .file_uploader import FileUploader
from .floating_menu import FloatingMenu
from .forgot_password import ForgotPassword
from .login_page import LoginPage
from .frame import FrameHandler
from .geo_location import GeoLocation
from .horizontal_slider import HorizontalSlider

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
    # DragAndDrop,
    # Dropdown,
    # DynamicContent,
    # DynamicControls,
    # DynamicLoading,
    # EntryAd,
    # ExitIntent,
    # FileDownloader,
    # FileUploader,
    # FloatingMenu,
    # ForgotPassword,
    # LoginPage,
    # FrameHandler,
    # GeoLocation,
    HorizontalSlider,
]