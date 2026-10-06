from typing import Final

from interface._constants import WINDOW_HEIGHT, WINDOW_WIDTH


CLASS_LABELS = (
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'd', 'e',
    'f', 'g', 'h', 'n', 'q', 'r', 't'
)

NUM_CLASSES: Final[int] = 47
NUM_COLUMNS: Final[int] = NUM_CLASSES

BODY_COLOR_LIGHTEN: Final[int] = 20
BODY_HEIGHT: Final[int] = WINDOW_HEIGHT

BODY_PADDING: Final[int] = 0
BODY_SPACE_BETWEEN: Final[int] = 0

MATRIX_PANEL_PADDING: Final[int] = 0
MATRIX_PANEL_CORNERS_RADIUS: Final[int] = 0
MATRIX_PANEL_COLOR_LIGHTEN: Final[int] = 20
MATRIX_HEADER_ROW_HEIGHT: Final[int] = 24
MATRIX_LABEL_COLUMN_WIDTH: Final[int] = 34

CLOSE_BUTTON_WIDTH: Final[int] = MATRIX_LABEL_COLUMN_WIDTH
CLOSE_BUTTON_HEIGHT: Final[int] = MATRIX_HEADER_ROW_HEIGHT
CLOSE_BUTTON_TEXT: Final[str] = "X"
CLOSE_BUTTON_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)
CLOSE_BUTTON_CORNERS_RADIUS: Final[int] = 0
CLOSE_BUTTON_FONT_SIZE: Final[int] = 15

_CONTENT_WIDTH: Final[int] = WINDOW_WIDTH - 2 * BODY_PADDING
_GRID_AVAILABLE_WIDTH: Final[int] = (
    _CONTENT_WIDTH - 2 * MATRIX_PANEL_PADDING - MATRIX_LABEL_COLUMN_WIDTH
)
CELL_WIDTH: Final[int] = _GRID_AVAILABLE_WIDTH // NUM_COLUMNS
_WIDTH_REMAINDER: Final[int] = _GRID_AVAILABLE_WIDTH % NUM_COLUMNS
COLUMN_WIDTHS: Final[tuple[int, ...]] = tuple(
    CELL_WIDTH + (1 if index < _WIDTH_REMAINDER else 0)
    for index in range(NUM_COLUMNS)
)

_AVAILABLE_HEIGHT: Final[int] = BODY_HEIGHT - 2 * BODY_PADDING
_GRID_AVAILABLE_HEIGHT: Final[int] = (
    _AVAILABLE_HEIGHT - 2 * MATRIX_PANEL_PADDING - MATRIX_HEADER_ROW_HEIGHT
)
CELL_HEIGHT: Final[int] = _GRID_AVAILABLE_HEIGHT // NUM_CLASSES
_HEIGHT_REMAINDER: Final[int] = _GRID_AVAILABLE_HEIGHT % NUM_CLASSES
ROW_HEIGHTS: Final[tuple[int, ...]] = tuple(
    CELL_HEIGHT + (1 if index < _HEIGHT_REMAINDER else 0)
    for index in range(NUM_CLASSES)
)
CELL_BRIGHTNESS_ON_HOVER: Final[int] = 20

MATRIX_GRID_WIDTH: Final[int] = MATRIX_LABEL_COLUMN_WIDTH + sum(COLUMN_WIDTHS)
MATRIX_PANEL_WIDTH: Final[int] = MATRIX_GRID_WIDTH + 2 * MATRIX_PANEL_PADDING
MATRIX_PANEL_HEIGHT: Final[int] = (
    2 * MATRIX_PANEL_PADDING + MATRIX_HEADER_ROW_HEIGHT + sum(ROW_HEIGHTS)
)

MATRIX_LABEL_FONT_SIZE: Final[int] = 14
MATRIX_LABEL_TEXT_COLOR: Final[tuple[int, int, int]] = (255, 255, 255)

MATRIX_ZERO_CELL_COLOR: Final[tuple[int, int, int]] = (45, 45, 45)
MATRIX_MAX_CELL_COLOR: Final[tuple[int, int, int]] = (252, 70, 48)
MATRIX_CELL_CORNERS_RADIUS: Final[int] = 2

CELL_MODAL_WIDTH: Final[int] = 320
CELL_MODAL_HEIGHT: Final[int] = 150
CELL_MODAL_PADDING: Final[int] = 20
CELL_MODAL_SPACE_BETWEEN: Final[int] = 12
CELL_MODAL_CORNERS_RADIUS: Final[int] = 20
CELL_MODAL_TITLE_FONT_SIZE: Final[int] = 24
CELL_MODAL_TEXT_FONT_SIZE: Final[int] = 20
CELL_MODAL_CLOSE_BUTTON_WIDTH: Final[int] = 70
CELL_MODAL_CLOSE_BUTTON_HEIGHT: Final[int] = 40
CELL_MODAL_CLOSE_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    10, 10, 10, 10)

MODAL_OVERLAY_COLOR: Final[tuple[int, int, int, int]] = (0, 0, 0, 150)
MODAL_BACKGROUND_COLOR_LIGHTEN: Final[int] = 20
