from dataclasses import dataclass
from typing import Any, Callable, Final
from interface._constants import WINDOW_HEIGHT, WINDOW_WIDTH, HEADER_HEIGHT

BODY_COLOR_LIGHTEN: Final[int] = 20
BODY_HEIGHT: Final[int] = WINDOW_HEIGHT - HEADER_HEIGHT

BUTTONS_CONTAINER_WIDTH_RATIO: Final[float] = 2
BUTTONS_CONTAINER_HEIGHT_RATIO: Final[float] = 1.3
BUTTONS_CONTAINER_SPACE_BETWEEN: Final[int] = 24
BUTTONS_CONTAINER_CORNERS_RADIUS: Final[int] = 40
BUTTONS_CONTAINER_WIDTH: Final[int] = int(
    WINDOW_WIDTH / BUTTONS_CONTAINER_WIDTH_RATIO
)
BUTTONS_CONTAINER_HEIGHT: Final[int] = int(
    BODY_HEIGHT / BUTTONS_CONTAINER_HEIGHT_RATIO
)

ACTION_BUTTON_WIDTH_RATIO: Final[float] = 1.5
ACTION_BUTTON_HEIGHT_RATIO: Final[float] = 4.7
ACTION_BUTTON_FONT_SIZE: Final[int] = 40

START_BUTTON_TEXT: Final[str] = "START"
START_BUTTON_COLOR: Final[tuple[int, int, int]] = (255, 147, 23)
START_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (20, 20, 0, 0)

METRICS_BUTTON_TEXT: Final[str] = "METRICS"
METRICS_BUTTON_COLOR: Final[tuple[int, int, int]] = (252, 70, 48)
METRICS_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (0, 0, 0, 0)

EXIT_BUTTON_TEXT: Final[str] = "EXIT"
EXIT_BUTTON_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)
EXIT_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (0, 0, 20, 20)


@dataclass(frozen=True, slots=True)
class ActionButtonSpec:
    text: str
    corners_radius: tuple[int, int, int, int]
    color: tuple[int, int, int]
    action: Callable[[], Any]
