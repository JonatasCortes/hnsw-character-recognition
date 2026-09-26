from dataclasses import dataclass
from typing import Any, Callable, Final
from interface._constants import WINDOW_HEIGHT, HEADER_HEIGHT

CORRECT_COLOR: Final[tuple[int, int, int]] = (120, 208, 98)
INCORRECT_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)

BODY_COLOR_LIGHTEN: Final[int] = 15
# cor dos "cards" (welcome, inputs, botões), mais clara que o body
CARD_COLOR_LIGHTEN: Final[int] = 35

BODY_HEIGHT: Final[int] = WINDOW_HEIGHT - HEADER_HEIGHT
BODY_PADDING: Final[int] = 40
BODY_SPACE_BETWEEN: Final[int] = 40

WELCOME_MESSAGE_WIDTH_RATIO: Final[float] = 0.75
WELCOME_MESSAGE_HEIGHT_RATIO: Final[int] = 3
WELCOME_MESSAGE_PADDING: Final[tuple[int, int, int, int]] = (0, 0, 0, 60)
WELCOME_MESSAGE_SPACE_BETWEEN: Final[int] = 8
WELCOME_MESSAGE_CORNERS_RADIUS: Final[int] = 20
WELCOME_MESSAGE_FONT_SIZE: Final[int] = 22

# cores de destaque para os parâmetros no texto de boas-vindas
M_HIGHLIGHT_COLOR: Final[tuple[int, int, int]] = (255, 183, 3)     # âmbar
EF_HIGHLIGHT_COLOR: Final[tuple[int, int, int]] = (76, 201, 240)   # ciano

INPUT_CONTAINER_PADDING: Final[int] = 20
INPUT_CONTAINER_CORNERS_RADIUS: Final[int] = 20
INPUT_CONTAINER_SPACE_BETWEEN: Final[int] = 40

INPUT_WIDTH: Final[int] = 300
INPUT_HEIGHT: Final[int] = 50
INPUT_CORNER_RADIUS: Final[int] = 20
INPUT_LABEL_FONT_SIZE: Final[int] = 18
INPUT_LABEL_HEIGHT: Final[int] = 26
INPUT_LABEL_SPACE_BETWEEN: Final[int] = 10

M_LABEL_TEXT: Final[str] = "M"
EF_CONSTRUCTION_LABEL_TEXT: Final[str] = "efConstruction"

BUTTONS_CONTAINER_WIDTH: Final[int] = 400
BUTTON_HEIGHT: Final[int] = 70
BUTTONS_CONTAINER_PADDING: Final[int] = 15
BUTTONS_CONTAINER_HEIGHT: Final[int] = BUTTON_HEIGHT + \
    2 * BUTTONS_CONTAINER_PADDING
BUTTONS_CONTAINER_CORNERS_RADIUS: Final[int] = 30
BUTTONS_CONTAINER_SPACE_BETWEEN: Final[int] = 30
ACTION_BUTTON_FONT_SIZE: Final[int] = 26

EXIT_BUTTON_TEXT: Final[str] = "EXIT"
EXIT_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (20, 0, 20, 0)
BUILD_BUTTON_TEXT: Final[str] = "BUILD"
BUILD_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (0, 20, 0, 20)


@dataclass(frozen=True, slots=True)
class ActionButtonSpec:
    text: str
    color: tuple[int, int, int]
    corners_radius: tuple[int, int, int, int]
    action: Callable[[], Any]
