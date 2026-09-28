from typing import Final
from desklab import Window, Color, Font
from pathlib import Path

DEFAULT_DATABASE_PATH: Final[Path] = Path("hnsw.json")
DEFAULT_TEST_RESULTS_PATH: Final[Path] = Path("hnsw_tests.json")

WINDOW_WIDTH: Final[int] = 1000
WINDOW_HEIGHT: Final[int] = 800
WINDOW_CAPTION: Final[str] = "hnsw-character-recognition"

Window.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption=WINDOW_CAPTION)

BASE_COLOR: Final[Color] = Color((51, 36, 43))
DEFAULT_FONT: Final[Font] = Font("consolas", 40)
HEADER_HEIGHT: Final[int] = 100

SETUP = True
