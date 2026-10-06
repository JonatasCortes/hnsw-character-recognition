from dataclasses import dataclass
from typing import Any, Callable, Final

from interface._constants import HEADER_HEIGHT, WINDOW_HEIGHT, WINDOW_WIDTH

BODY_COLOR_LIGHTEN: Final[int] = 20
BODY_HEIGHT: Final[int] = WINDOW_HEIGHT - HEADER_HEIGHT
BODY_PADDING: Final[int] = 30
CONTAINERS_SPACE_BETWEEN: Final[int] = 30

CONTAINER_CORNERS_RADIUS: Final[int] = 30
CONTAINER_WIDTH: Final[int] = (
    WINDOW_WIDTH - 2 * BODY_PADDING - CONTAINERS_SPACE_BETWEEN
) // 2
CONTAINER_HEIGHT: Final[int] = BODY_HEIGHT - 2 * BODY_PADDING

TITLE_BAR_HEIGHT: Final[int] = 60
TITLE_BAR_COLOR_LIGHTEN: Final[int] = 10
TITLE_FONT_SIZE: Final[int] = 26
TITLE_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (30, 30, 0, 0)
PARAMETERS_TITLE: Final[str] = "PARAMETERS"
METRICS_TITLE: Final[str] = "RESULTS"

CARDS_AREA_PADDING: Final[int] = 20
CARDS_AREA_SPACE_BETWEEN: Final[int] = 10
CARDS_AREA_HEIGHT: Final[int] = CONTAINER_HEIGHT - TITLE_BAR_HEIGHT
CARDS_AREA_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (0, 0, 30, 30)

CARDS_PER_CONTAINER: Final[int] = 7
CARD_WIDTH: Final[int] = CONTAINER_WIDTH - 2 * CARDS_AREA_PADDING
CARD_HEIGHT: Final[int] = (
    CARDS_AREA_HEIGHT - 2 * CARDS_AREA_PADDING
    - (CARDS_PER_CONTAINER - 1) * CARDS_AREA_SPACE_BETWEEN
) // CARDS_PER_CONTAINER

LABEL_BOX_WIDTH: Final[int] = CARD_WIDTH * 3 // 5
VALUE_BOX_WIDTH: Final[int] = CARD_WIDTH - LABEL_BOX_WIDTH
LABEL_BOX_COLOR_LIGHTEN: Final[int] = 10
VALUE_BOX_COLOR_LIGHTEN: Final[int] = 30
LABEL_BOX_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (15, 0, 15, 0)
VALUE_BOX_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (0, 15, 0, 15)

LABEL_FONT_SIZE: Final[int] = 20
VALUE_FONT_SIZE: Final[int] = 28
TEXT_COLOR: Final[tuple[int, int, int]] = (255, 255, 255)

CONFUSION_MATRIX_BUTTON_TEXT: Final[str] = "CONFUSION MATRIX"
CONFUSION_MATRIX_BUTTON_COLOR: Final[tuple[int, int, int]] = (252, 70, 48)
RETURN_BUTTON_TEXT: Final[str] = "RETURN"
RETURN_BUTTON_COLOR: Final[tuple[int, int, int]] = (227, 8, 66)
ACTION_BUTTON_FONT_SIZE: Final[int] = 23
ACTION_BUTTON_CORNERS_RADIUS: Final[tuple[int, int, int, int]] = (
    15, 15, 15, 15)
CONFUSION_MATRIX_BUTTON_WIDTH: Final[int] = (
    (CARD_WIDTH - CARDS_AREA_SPACE_BETWEEN) * 3 // 5
)
RETURN_BUTTON_WIDTH: Final[int] = (
    CARD_WIDTH - CARDS_AREA_SPACE_BETWEEN - CONFUSION_MATRIX_BUTTON_WIDTH
)

DEFAULT_METRIC_VALUE: Final[str] = "N/A"
CORRECT_COLOR: Final[tuple[int, int, int]] = (93, 114, 77)
INCORRECT_COLOR: Final[tuple[int, int, int]] = (135, 35, 64)


@dataclass(frozen=True, slots=True)
class ResultField:
    key: str
    label: str
    format_value: Callable[[Any], str] = str
    accent_color: tuple[int, int, int] | None = None


PARAMETER_FIELDS: Final[tuple[ResultField, ...]] = (
    ResultField("max_neighbors", "MAX NEIGHBORS"),
    ResultField("construction_max_candidates", "BUILD CANDIDATES"),
    ResultField("classification_max_candidates", "SEARCH CANDIDATES"),
    ResultField("image_sections", "IMAGE SECTIONS"),
    ResultField("luminance_threshold", "LUMINANCE THRESHOLD"),
    ResultField("layer_growth_factor", "LAYER GROWTH FACTOR"),
    ResultField("shuffle_seed", "SHUFFLE SEED"),
)

METRIC_FIELDS: Final[tuple[ResultField, ...]] = (
    ResultField("total_tests", "TOTAL TESTS", lambda value: f"{value}"),
    ResultField("total_correct", "CORRECT",
                lambda value: f"{value}", CORRECT_COLOR),
    ResultField("total_incorrect", "INCORRECT",
                lambda value: f"{value}", INCORRECT_COLOR),
    ResultField("accuracy", "ACCURACY", lambda value: f"{value * 100:.2f}%"),
    ResultField("execution_time_per_test", "TIME PER TEST",
                lambda value: f"{value * 1000:.3f} ms"),
    ResultField("total_execution_time", "TOTAL TIME",
                lambda value: f"{value:.2f} s"),
)
