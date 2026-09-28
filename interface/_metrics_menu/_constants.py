from dataclasses import dataclass
from typing import Final

from interface._constants import WINDOW_HEIGHT, WINDOW_WIDTH, HEADER_HEIGHT


BODY_COLOR_LIGHTEN: Final[int] = 20
BODY_HEIGHT: Final[int] = WINDOW_HEIGHT - HEADER_HEIGHT


BUTTONS_CONTAINER_WIDTH_RATIO: Final[float] = 2
BUTTONS_CONTAINER_HEIGHT_RATIO: Final[float] = 1.3
BUTTONS_CONTAINER_SPACE_BETWEEN: Final[int] = 24
BUTTONS_CONTAINER_CORNERS_RADIUS: Final[int] = 40
BUTTONS_CONTAINER_PADDING: Final[tuple[int, int, int, int]] = (20, 0, 20, 0)
BUTTONS_CONTAINER_WIDTH: Final[int] = int(
    WINDOW_WIDTH / BUTTONS_CONTAINER_WIDTH_RATIO)
BUTTONS_CONTAINER_HEIGHT: Final[int] = int(
    BODY_HEIGHT / BUTTONS_CONTAINER_HEIGHT_RATIO)

ACTION_BUTTON_WIDTH_RATIO: Final[float] = 1.5
ACTION_BUTTON_WIDTH: Final[int] = int(
    BUTTONS_CONTAINER_WIDTH / ACTION_BUTTON_WIDTH_RATIO)
ACTION_BUTTON_FONT_SIZE: Final[int] = 32


NUM_ITEMS: Final[int] = 4
_VERTICAL_PADDING: Final[int] = BUTTONS_CONTAINER_PADDING[0] + \
    BUTTONS_CONTAINER_PADDING[2]
_GAPS: Final[int] = (NUM_ITEMS - 1) * BUTTONS_CONTAINER_SPACE_BETWEEN
ITEM_HEIGHT: Final[int] = (
    BUTTONS_CONTAINER_HEIGHT - _VERTICAL_PADDING - _GAPS
) // NUM_ITEMS

ACTION_BUTTON_HEIGHT: Final[int] = ITEM_HEIGHT
ACCURACY_CARD_HEIGHT: Final[int] = ITEM_HEIGHT
ACCURACY_CARD_WIDTH: Final[int] = ACTION_BUTTON_WIDTH

ACCURACY_CARD_PADDING: Final[int] = 18
ACCURACY_CARD_INNER_SPACE_BETWEEN: Final[int] = 10

ACCURACY_LABEL_FONT_SIZE: Final[int] = 18
ACCURACY_VALUE_FONT_SIZE: Final[int] = 36
ACCURACY_TEXT_COLOR: Final[tuple[int, int, int]] = (255, 255, 255)

DEFAULT_METRIC_VALUE: Final[str] = "N/A"

VERIFIED_ACCURACY_LABEL: Final[str] = "VERIFIED ACCURACY"
PRACTICAL_ACCURACY_LABEL: Final[str] = "PRACTICAL ACCURACY"

VERIFIED_ACCURACY_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    20, 20, 0, 0)
PRACTICAL_ACCURACY_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    0, 0, 20, 20)

CONFUSION_MATRIX_BUTTON_TEXT: Final[str] = "CONFUSION MATRIX"
CONFUSION_MATRIX_BUTTON_COLOR: Final[tuple[int, int, int]] = (252, 70, 48)
CONFUSION_MATRIX_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    20, 20, 0, 0)

RETURN_BUTTON_TEXT: Final[str] = "RETURN"
RETURN_BUTTON_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)
RETURN_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (0, 0, 20, 20)


@dataclass(frozen=True, slots=True)
class AccuracyCardSpec:
    label: str
    value: str
    accent_color: tuple[int, ...]
    corners_radius: tuple[int, int, int, int]
