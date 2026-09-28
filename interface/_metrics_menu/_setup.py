import json
from typing import Callable, Final

from . import _constants as const
from desklab import FlexBox, Text, Window
from interface._utils import create_button_with_text, build_header
from interface._constants import WINDOW_WIDTH, BASE_COLOR, DEFAULT_FONT, DEFAULT_TEST_RESULTS_PATH


metrics_menu: Final[Window] = Window()


def _build_accuracy_card(spec: const.AccuracyCardSpec) -> FlexBox:
    card = FlexBox(
        const.ACCURACY_CARD_WIDTH, const.ACCURACY_CARD_HEIGHT,
        padding=const.ACCURACY_CARD_PADDING,
        space_between=const.ACCURACY_CARD_INNER_SPACE_BETWEEN,
        corners_radius=spec.corners_radius,
        color=spec.accent_color,
    )

    label_text = Text(spec.label, DEFAULT_FONT.copy(
        size=const.ACCURACY_LABEL_FONT_SIZE), const.ACCURACY_TEXT_COLOR)
    value_text = Text(spec.value, DEFAULT_FONT.copy(
        size=const.ACCURACY_VALUE_FONT_SIZE), const.ACCURACY_TEXT_COLOR)
    card.add_children([label_text, value_text])

    return card


def _load_verified_accuracy() -> str:
    try:
        with DEFAULT_TEST_RESULTS_PATH.open(mode="r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return const.DEFAULT_METRIC_VALUE

    return f"{data['acuracy'] * 100:.2f}%"


def _build_buttons_container(
    width: int,
    height: int,
    verified_accuracy: str,
    open_confusion_matrix: Callable[[], None],
) -> FlexBox:
    container = FlexBox(
        width, height, const.BUTTONS_CONTAINER_PADDING,
        space_between=const.BUTTONS_CONTAINER_SPACE_BETWEEN,
        corners_radius=const.BUTTONS_CONTAINER_CORNERS_RADIUS,
        color=BASE_COLOR,
    )

    verified_card = _build_accuracy_card(
        const.AccuracyCardSpec(
            const.VERIFIED_ACCURACY_LABEL, verified_accuracy,
            BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN).get_tuple(),
            const.VERIFIED_ACCURACY_CORNERS_RADIUS,
        )
    )

    practical_card = _build_accuracy_card(
        const.AccuracyCardSpec(
            const.PRACTICAL_ACCURACY_LABEL, const.DEFAULT_METRIC_VALUE,
            BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN).get_tuple(),
            const.PRACTICAL_ACCURACY_CORNERS_RADIUS,
        )
    )

    confusion_matrix_button = create_button_with_text(
        const.ACTION_BUTTON_WIDTH, const.ACTION_BUTTON_HEIGHT,
        const.CONFUSION_MATRIX_BUTTON_COLOR, const.CONFUSION_MATRIX_BUTTON_TEXT,
        corners_radius=const.CONFUSION_MATRIX_BUTTON_CORNERS_RADIUS,
        font_size=const.ACTION_BUTTON_FONT_SIZE, action=open_confusion_matrix,
    )

    return_button = create_button_with_text(
        const.ACTION_BUTTON_WIDTH, const.ACTION_BUTTON_HEIGHT,
        const.RETURN_BUTTON_COLOR, const.RETURN_BUTTON_TEXT,
        corners_radius=const.RETURN_BUTTON_CORNERS_RADIUS,
        font_size=const.ACTION_BUTTON_FONT_SIZE, action=metrics_menu.close,
    )

    container.add_children(
        [verified_card, practical_card, confusion_matrix_button, return_button])

    return container


def metrics_menu_setup(confusion_matrix_menu: Window) -> Window:
    base_layer = metrics_menu.add_layer()

    header = build_header(WINDOW_WIDTH)
    body = FlexBox(WINDOW_WIDTH, const.BODY_HEIGHT,
                   color=BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN))

    verified_accuracy = _load_verified_accuracy()

    buttons_container = _build_buttons_container(
        const.BUTTONS_CONTAINER_WIDTH,
        const.BUTTONS_CONTAINER_HEIGHT,
        verified_accuracy,
        confusion_matrix_menu.open,
    )
    body.add_children(buttons_container)

    base_layer.add_children([header, body])
    return metrics_menu
