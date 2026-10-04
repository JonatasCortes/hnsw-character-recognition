from ._constants import SETUP, DEFAULT_DATABASE_PATH
from ._hnsw_customization_menu import hnsw_customization_menu_setup
from ._classify_menu import classify_menu_setup
from ._main_menu import main_menu_setup
from ._metrics_menu import metrics_menu_setup
from ._confusion_matrix_menu import confusion_matrix_menu_setup

assert SETUP
if not DEFAULT_DATABASE_PATH.exists():
    HNSW_CUSTOMIZATION_MENU = hnsw_customization_menu_setup()
    HNSW_CUSTOMIZATION_MENU.open()
CLASSIFY_MENU = classify_menu_setup()
CONFUSION_MATRIX_MENU = confusion_matrix_menu_setup()
METRICS_MENU = metrics_menu_setup(CONFUSION_MATRIX_MENU)
MAIN_MENU = main_menu_setup(CLASSIFY_MENU, METRICS_MENU)

__all__ = [
    "MAIN_MENU"
]
