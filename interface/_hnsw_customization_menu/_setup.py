from . import _constants as const
from typing import Any, Final
from desklab import FlexBox, Window, Text, Font, Color, TextInput
from interface._utils import build_header, create_button_with_text
from interface._constants import WINDOW_WIDTH, BASE_COLOR, DEFAULT_FONT
from interface._loading_menu import loading_menu_setup
from src.hnsw import HnswParameters
import sys


hnsw_customization_menu: Final[Window] = Window()


def _build_labeled_input_stack(labels: tuple[str, ...], text_inputs: list[TextInput], color: Color) -> FlexBox:
    stack = FlexBox(const.INPUT_WIDTH,
                    const.INPUT_CONTAINER_HEIGHT,
                    space_between=const.INPUT_CONTAINER_SPACE_BETWEEN,
                    color=color)
    for label, text_input in zip(labels, text_inputs):
        labeled_input = _build_labeled_input(label, text_input, color)
        stack.add_children(labeled_input)
    return stack


def _build_labeled_input(label: str, text_input: TextInput, color: Color) -> FlexBox:
    label_text = Text(label, DEFAULT_FONT.copy(size=17), const.LABEL_COLOR)
    container = FlexBox(const.INPUT_WIDTH,
                        text_input.get_height() + label_text.get_height() +
                        const.LABELED_INPUT_SPACE_BETWEEN,
                        horizontal_alignment=const.LABELED_INPUT_HORIZONTAL_ALIGNMENT,
                        space_between=const.LABELED_INPUT_SPACE_BETWEEN,
                        color=color)
    container.add_children([label_text, text_input])
    return container


def _build_welcome_message(width: int, height: int, color: Color) -> FlexBox:
    welcome_message = FlexBox(width, height,
                              padding=const.WELCOME_MESSAGE_PADDING,
                              flex_direction="COLUMN", horizontal_alignment="LEFT",
                              space_between=const.WELCOME_MESSAGE_SPACE_BETWEEN,
                              corners_radius=const.WELCOME_MESSAGE_CORNERS_RADIUS,
                              color=color)

    font = Font("consolas", const.WELCOME_MESSAGE_FONT_SIZE)
    welcome_message.add_children(
        [
            Text(text, font, (15*i, 255, 255 - i*15))
            for i, text in enumerate((
                "Welcome to the HNSW Customization Menu!",
                "Configure the database parameters below:",
                f"    1 - {const.MAX_NEIGHBORS_LABEL} (Maximum number of connections per node)",
                f"    2 - {const.CONSTRUCTION_MAX_CANDIDATES_LABEL} (Number of candidates during build)",
                f"    3 - {const.CLASSIFICATION_MAX_CANDIDATES_LABEL} (Candidates examined during query)",
                f"    4 - {const.IMAGE_SECTIONS_LABEL} (Grid partitions per image sample)",
                f"    5 - {const.LUMINANCE_THRESHOLD_LABEL} (Pixel filter threshold value)",
                f"    6 - {const.LAYER_GROWTH_FACTOR_LABEL} (OPTIONAL: Default = {const.MAX_NEIGHBORS_LABEL})"
            ))
        ]
    )
    return welcome_message


def _build_hnsw(inputs: list[TextInput], labels: tuple[str, ...]) -> None:
    parameter_map: dict[str, Any] = {}
    for input_field, label in zip(inputs, labels):
        input_value = input_field.get_text()
        if label == const.LAYER_GROWTH_FACTOR_LABEL and input_value == "":
            parameter_map[label.lower()] = None
            continue
        if not input_value.isdigit():
            return
        parameter_map[label.lower()] = int(input_value)

    parameters = HnswParameters(**parameter_map)
    loading_menu = loading_menu_setup(parameters)
    hnsw_customization_menu.close()
    loading_menu.open()


def hnsw_customization_menu_setup() -> Window:
    base_layer = hnsw_customization_menu.add_layer()
    body_color = BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN)
    welcome_container_color = BASE_COLOR.lightened(
        const.WELCOME_MESSAGE_COLOR_LIGHTEN)

    header = build_header(WINDOW_WIDTH)

    body = FlexBox(WINDOW_WIDTH, const.BODY_HEIGHT, padding=const.BODY_PADDING,
                   space_between=const.BODY_SPACE_BETWEEN, color=body_color)

    content_width = int(WINDOW_WIDTH * const.WELCOME_MESSAGE_WIDTH_RATIO)
    welcome_message = _build_welcome_message(
        content_width, const.WELCOME_MESSAGE_HEIGHT, welcome_container_color,
    )

    input_container_color = BASE_COLOR.lightened(
        const.INPUT_CONTAINER_COLOR_LIGHTEN)
    input_container = FlexBox(content_width, const.INPUT_CONTAINER_HEIGHT,
                              flex_direction=const.INPUT_CONTAINER_FLEX_DIRECTION,
                              space_between=const.INPUT_CONTAINER_SPACE_BETWEEN,
                              corners_radius=const.INPUT_CONTAINER_CORNER_RADIUS,
                              color=input_container_color)

    inputs = [TextInput(const.INPUT_WIDTH, const.INPUT_HEIGHT, corners_radius=const.INPUT_CORNER_RADIUS)
              for _ in range(len(const.LABELS))]

    split = len(const.LABELS)//2
    first_input_stack = _build_labeled_input_stack(const.LABELS[:split],
                                                   inputs[:split],
                                                   input_container_color)
    seccond_input_stack = _build_labeled_input_stack(const.LABELS[split:],
                                                     inputs[split:],
                                                     input_container_color)

    start_button = create_button_with_text(const.BUTTON_WIDTH, const.BUTTON_HEIGHT,
                                           const.START_BUTTON_COLOR, "START",
                                           action=lambda: _build_hnsw(inputs, const.LABELS))
    exit_button = create_button_with_text(const.BUTTON_WIDTH, const.BUTTON_HEIGHT,
                                          const.EXIT_BUTTON_COLOR, "EXIT",
                                          action=lambda: sys.exit(0))

    buttons_container = FlexBox(const.BUTTON_WIDTH, const.BUTTON_HEIGHT*2 + const.BUTTON_CONTAINER_SPACE_BETWEEN,
                                color=input_container_color, space_between=const.BUTTON_CONTAINER_SPACE_BETWEEN)

    buttons_container.add_children([start_button, exit_button])
    input_container.add_children(
        [first_input_stack, seccond_input_stack, buttons_container])

    body.add_children([welcome_message, input_container])
    base_layer.add_children([header, body])
    return hnsw_customization_menu
