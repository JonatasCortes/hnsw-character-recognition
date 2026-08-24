from dataclasses import dataclass
from typing import Any, Callable, Final
from desklab import Font

CORRECT_COLOR: Final[tuple[int, int, int]] = (120, 208, 98)
INCORRECT_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)

DISPLAY_FONT: Final[Font] = Font("trebuchet", 150)
MODAL_TITLE_FONT_SIZE: Final[int] = 30
VERDICT_BUTTON_FONT_SIZE: Final[int] = 30

COLOR_PALETTE_HEIGHT: Final[int] = 70
COLOR_PALETTE_SPACE_BETWEEN: Final[int] = 20

ASSETS_PATH: Final[str] = "interface/_assets/"
TOOL_ICONS: Final[tuple[str, ...]] = ("pencil.png", "filler.png",
                                      "eraser.png", "clearer.png")
TOOL_BUTTON_SIZE: Final[int] = 50

BRUSH_BUTTON_SIZE: Final[int] = 50
BRUSH_BUTTON_CORNERS_RADIUS: Final[int] = 20

BRUSH_COLORS: Final[tuple[tuple[tuple[int, int, int], int], ...]] = (
    ((24, 18, 30), 15),
    ((244, 91, 105), 20),
    ((255, 183, 3), 40),
    ((33, 158, 188), 30),
    ((142, 202, 230), 40),
    ((29, 53, 87), 15),
    ((172, 96, 172), 20),
    ((138, 191, 126), 30),
    ((250, 240, 228), -300),
    ((224, 122, 95), 30),
)

DRAWING_AREA_WIDTH_RATIO: Final[float] = 1.5
DRAWING_AREA_PADDING: Final[int] = 0
DRAWING_AREA_COLOR_LIGHTEN: Final[int] = 30
DRAWING_AREA_ERASER_WIDTH: Final[int] = 20

INFO_MENU_PADDING: Final[tuple[int, int, int, int]] = (0, 0, 10, 0)
INFO_MENU_SPACE_BETWEEN: Final[int] = 30

CLASSIFICATION_DISPLAY_WIDTH_RATIO: Final[float] = 1.2
CLASSIFICATION_DISPLAY_HEIGHT_RATIO: Final[float] = 3
CLASSIFICATION_DISPLAY_COLOR_LIGHTEN: Final[int] = 20
CLASSIFICATION_DISPLAY_DEFAULT_TEXT: Final[str] = "N/A"
CLASSIFICATION_DISPLAY_CORNERS_RADIUS: Final[int] = 40

BUTTONS_CONTAINER_WIDTH_RATIO: Final[float] = 1.2
BUTTONS_CONTAINER_HEIGHT_RATIO: Final[float] = 2
BUTTONS_CONTAINER_SPACE_BETWEEN: Final[int] = 20
BUTTONS_CONTAINER_CORNERS_RADIUS: Final[int] = 40
BUTTONS_CONTAINER_COLOR_LIGHTEN: Final[int] = 10

ACTION_BUTTON_WIDTH_RATIO: Final[float] = 1.44
ACTION_BUTTON_HEIGHT_RATIO: Final[float] = 6

CLASSIFY_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    20, 20, 0, 0
)
RETURN_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (0, 0, 20, 20)

MODAL_WIDTH: Final[int] = 500
MODAL_HEIGHT: Final[int] = 500
MODAL_HEADER_HEIGHT: Final[int] = 70
MODAL_BODY_HEIGHT: Final[int] = MODAL_HEIGHT - MODAL_HEADER_HEIGHT
MODAL_BODY_PADDING: Final[int] = 25
MODAL_BODY_SPACE_BETWEEN: Final[int] = 25
MODAL_CONTENT_WIDTH: Final[int] = MODAL_WIDTH - 2 * MODAL_BODY_PADDING

MODAL_OVERLAY_COLOR: Final[tuple[int, int, int, int]] = (0, 0, 0, 150)
MODAL_BACKGROUND_COLOR_LIGHTEN: Final[int] = 70
MODAL_HEADER_SPACE_BETWEEN: Final[int] = 70
MODAL_HEADER_COLOR_LIGHTEN: Final[int] = 20
MODAL_TITLE_TEXT: Final[str] = "CLASSIFICATION"

CLOSE_MODAL_BUTTON_WIDTH: Final[int] = 70
CLOSE_MODAL_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    10, 0, 0, 0
)
CLOSE_MODAL_BUTTON_TEXT: Final[str] = "X"

RESULT_DISPLAY_COLOR_LIGHTEN: Final[int] = 40
RESULT_DISPLAY_CORNERS_RADIUS: Final[int] = 30
RESULT_DISPLAY_DEFAULT_TEXT: Final[str] = "N/A"

VERDICT_CONTAINER_HEIGHT: Final[int] = 120
VERDICT_BUTTON_HEIGHT: Final[int] = 80
VERDICT_BUTTON_SPACE_BETWEEN: Final[int] = 20
VERDICT_BUTTONS_PADDING: Final[int] = 15
VERDICT_BUTTONS_CORNERS_RADIUS: Final[int] = 30
VERDICT_BUTTONS_COLOR_LIGHTEN: Final[int] = 20
VERDICT_CORRECT_TEXT: Final[str] = "CORRECT"
VERDICT_INCORRECT_TEXT: Final[str] = "INCORRECT"
VERDICT_CORRECT_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    20, 0, 20, 0
)
VERDICT_INCORRECT_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    0, 20, 0, 20
)

RESULT_DISPLAY_HEIGHT: Final[int] = (
    MODAL_BODY_HEIGHT - 2 * MODAL_BODY_PADDING -
    MODAL_BODY_SPACE_BETWEEN - VERDICT_CONTAINER_HEIGHT
)


@dataclass(frozen=True, slots=True)
class ActionButtonSpec:
    text: str
    color: tuple[int, int, int]
    corners_radius: tuple[int, int, int, int]
    action: Callable[[], Any]
