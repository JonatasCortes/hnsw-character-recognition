from typing import Final

from desklab import Font
from interface._constants import HEADER_HEIGHT, WINDOW_HEIGHT, WINDOW_WIDTH

CANVAS_COLOR: Final[tuple[int, int, int]] = (0, 0, 0)
BRUSH_COLOR: Final[tuple[int, int, int]] = (255, 255, 255)
BRUSH_WIDTH: Final[int] = 50
ERASER_WIDTH: Final[int] = 70

RETURN_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)
TOOLBAR_LIGHTEN: Final[int] = 10
PANEL_LIGHTEN: Final[int] = 20
DISPLAY_LIGHTEN: Final[int] = 40

ASSETS_PATH: Final[str] = "interface/_assets/"
TOOL_ICONS: Final[tuple[str, ...]] = (
    "pencil.png", "eraser.png", "clearer.png")
TOOL_BUTTON_SIZE: Final[int] = 50
TOOLBAR_HEIGHT: Final[int] = 70
TOOLBAR_SPACE_BETWEEN: Final[int] = 30

BODY_HEIGHT: Final[int] = WINDOW_HEIGHT - HEADER_HEIGHT - TOOLBAR_HEIGHT
CANVAS_WIDTH: Final[int] = int(WINDOW_WIDTH / 1.5)
PANEL_WIDTH: Final[int] = WINDOW_WIDTH - CANVAS_WIDTH
PANEL_PADDING: Final[int] = 25
PANEL_SPACE_BETWEEN: Final[int] = 25
PANEL_CONTENT_WIDTH: Final[int] = PANEL_WIDTH - 2 * PANEL_PADDING

RETURN_BUTTON_HEIGHT: Final[int] = 90
RETURN_BUTTON_TEXT: Final[str] = "RETURN"
RETURN_BUTTON_CORNERS_RADIUS: Final[int] = 30
DISPLAY_HEIGHT: Final[int] = (
    BODY_HEIGHT - 2 * PANEL_PADDING - PANEL_SPACE_BETWEEN - RETURN_BUTTON_HEIGHT
)
DISPLAY_CORNERS_RADIUS: Final[int] = 40
DISPLAY_DEFAULT_TEXT: Final[str] = "N/A"
DISPLAY_FONT: Final[Font] = Font("trebuchet", 150)
