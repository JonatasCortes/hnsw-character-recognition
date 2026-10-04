from dataclasses import dataclass
from typing import Any, Callable, Final
from interface._constants import WINDOW_HEIGHT, HEADER_HEIGHT

CORRECT_COLOR: Final[tuple[int, int, int]] = (120, 208, 98)
INCORRECT_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)

BODY_COLOR_LIGHTEN: Final[int] = 15
CARD_COLOR_LIGHTEN: Final[int] = 30

BODY_HEIGHT: Final[int] = WINDOW_HEIGHT - HEADER_HEIGHT
BODY_PADDING: Final[int] = 15
BODY_SPACE_BETWEEN: Final[int] = 15

# Mensagem de boas-vindas otimizada para caber 6 linhas de texto de forma compacta
WELCOME_MESSAGE_WIDTH_RATIO: Final[float] = 0.85
WELCOME_MESSAGE_HEIGHT: Final[int] = 175
WELCOME_MESSAGE_PADDING: Final[tuple[int, int, int, int]] = (12, 15, 12, 15)
WELCOME_MESSAGE_SPACE_BETWEEN: Final[int] = 5
WELCOME_MESSAGE_CORNERS_RADIUS: Final[int] = 15
WELCOME_MESSAGE_FONT_SIZE: Final[int] = 16

# Cores de destaque atualizadas
M_HIGHLIGHT_COLOR: Final[tuple[int, int, int]] = (255, 183, 3)
EF_HIGHLIGHT_COLOR: Final[tuple[int, int, int]] = (76, 201, 240)
SECTION_HIGHLIGHT_COLOR: Final[tuple[int, int, int]] = (181, 23, 158)
THRESHOLD_HIGHLIGHT_COLOR: Final[tuple[int, int, int]] = (114, 9, 183)

# Inputs compactados verticalmente para suportar 5 itens sem estourar a tela de 800px
INPUT_CONTAINER_PADDING: Final[int] = 10
INPUT_CONTAINER_CORNERS_RADIUS: Final[int] = 15
INPUT_CONTAINER_SPACE_BETWEEN: Final[int] = 10

INPUT_HEIGHT: Final[int] = 36
INPUT_CORNER_RADIUS: Final[int] = 10
INPUT_LABEL_FONT_SIZE: Final[int] = 14
INPUT_LABEL_HEIGHT: Final[int] = 20
INPUT_LABEL_SPACE_BETWEEN: Final[int] = 4

MAX_NEIGHBORS_LABEL: Final[str] = "MAX_NEIGHBORS"
CONSTRUCTION_MAX_CANDIDATES_LABEL: Final[str] = "CONSTRUCTION_MAX_CANDIDATES"
CLASSIFICATION_MAX_CANDIDATES_LABEL: Final[str] = "CLASSIFICATION_MAX_CANDIDATES"
IMAGE_SECTIONS_LABEL: Final[str] = "IMAGE_SECTIONS"
LUMINANCE_THRESHOLD_LABEL: Final[str] = "LUMINANCE_THRESHOLD"

TEXT_INPUT_LABELS: Final[tuple[str, ...]] = (
    MAX_NEIGHBORS_LABEL,
    CONSTRUCTION_MAX_CANDIDATES_LABEL,
    CLASSIFICATION_MAX_CANDIDATES_LABEL,
    IMAGE_SECTIONS_LABEL,
    LUMINANCE_THRESHOLD_LABEL
)

BUTTONS_CONTAINER_WIDTH: Final[int] = 400
BUTTON_HEIGHT: Final[int] = 45
BUTTONS_CONTAINER_PADDING: Final[int] = 10
BUTTONS_CONTAINER_HEIGHT: Final[int] = BUTTON_HEIGHT + \
    (2 * BUTTONS_CONTAINER_PADDING)
BUTTONS_CONTAINER_CORNERS_RADIUS: Final[int] = 20
BUTTONS_CONTAINER_SPACE_BETWEEN: Final[int] = 20
ACTION_BUTTON_FONT_SIZE: Final[int] = 20

EXIT_BUTTON_TEXT: Final[str] = "EXIT"
EXIT_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (15, 0, 15, 0)
BUILD_BUTTON_TEXT: Final[str] = "BUILD"
BUILD_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (0, 15, 0, 15)


@dataclass(frozen=True, slots=True)
class ActionButtonSpec:
    text: str
    color: tuple[int, int, int]
    corners_radius: tuple[int, int, int, int]
    action: Callable[[], Any]
