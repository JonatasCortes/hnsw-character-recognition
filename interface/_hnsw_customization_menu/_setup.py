from . import _constants as const
from typing import Any, Callable, Final
from desklab import FlexBox, Window, TextInput, Text, Font, Color
from interface._utils import create_button_with_text, build_header
from interface._loading_menu import loading_menu_setup
from interface._constants import WINDOW_WIDTH, BASE_COLOR
import sys


hnsw_customization_menu: Final[Window] = Window()


def _build_welcome_message(width: int, height: int, color: Color) -> FlexBox:
    welcome_message = FlexBox(width, height,
                              padding=const.WELCOME_MESSAGE_PADDING,
                              flex_direction="COLUMN", horizontal_alignment="LEFT",
                              space_between=const.WELCOME_MESSAGE_SPACE_BETWEEN,
                              corners_radius=const.WELCOME_MESSAGE_CORNERS_RADIUS,
                              color=color)

    font = Font("trebuchet", const.WELCOME_MESSAGE_FONT_SIZE)
    welcome_message.add_children(
        [
            Text("Welcome to the HNSW Customization Menu! Select the desired",
                 font, "WHITE"),
            Text("parameters for your HNSW database below:", font, "WHITE"),
            Text("    1 - M (Maximum number of connections per node)",
                 font, const.M_HIGHLIGHT_COLOR),
            Text("    2 - efConstruction (Maximum number of neighbor",
                 font, const.EF_HIGHLIGHT_COLOR),
            Text("    candidates considered during each node insertion)",
                 font, const.EF_HIGHLIGHT_COLOR),
        ]
    )
    return welcome_message


def _build_labeled_input(label_text: str, font: Font) -> tuple[FlexBox, TextInput]:
    text_input = TextInput(const.INPUT_WIDTH, const.INPUT_HEIGHT,
                           corners_radius=const.INPUT_CORNER_RADIUS)

    labeled_input = FlexBox(
        const.INPUT_WIDTH,
        const.INPUT_HEIGHT + const.INPUT_LABEL_HEIGHT + const.INPUT_LABEL_SPACE_BETWEEN,
        space_between=const.INPUT_LABEL_SPACE_BETWEEN,
        horizontal_alignment="LEFT",
        color=BASE_COLOR,
    )
    labeled_input.add_children([Text(label_text, font, "WHITE"), text_input])
    return labeled_input, text_input


def _build_input_container() -> tuple[FlexBox, TextInput, TextInput]:
    input_container_width = int(WINDOW_WIDTH *
                                const.WELCOME_MESSAGE_WIDTH_RATIO)
    input_container_height = (const.INPUT_HEIGHT + const.INPUT_LABEL_HEIGHT +
                              const.INPUT_LABEL_SPACE_BETWEEN + 2 * const.INPUT_CONTAINER_PADDING)
    inputs_container = FlexBox(
        input_container_width,
        input_container_height,
        padding=const.INPUT_CONTAINER_PADDING,
        space_between=const.INPUT_CONTAINER_SPACE_BETWEEN, flex_direction="ROW",
        corners_radius=const.INPUT_CONTAINER_CORNERS_RADIUS, color=BASE_COLOR,
    )

    label_font = Font("trebuchet", const.INPUT_LABEL_FONT_SIZE)
    m_container, m_input = _build_labeled_input(
        const.M_LABEL_TEXT,
        label_font
    )
    ef_container, ef_input = _build_labeled_input(
        const.EF_CONSTRUCTION_LABEL_TEXT,
        label_font
    )

    inputs_container.add_children([m_container, ef_container])
    return inputs_container, m_input, ef_input


def _build_buttons_container(width: int, card_color: Color, on_build: Callable[[], Any], on_exit: Callable[[], Any]) -> FlexBox:
    buttons_container = FlexBox(width, const.BUTTONS_CONTAINER_HEIGHT,
                                padding=const.BUTTONS_CONTAINER_PADDING,
                                space_between=const.BUTTONS_CONTAINER_SPACE_BETWEEN,
                                flex_direction="ROW",
                                corners_radius=const.BUTTONS_CONTAINER_CORNERS_RADIUS,
                                color=card_color)

    specs: tuple[const.ActionButtonSpec, ...] = (
        const.ActionButtonSpec(const.EXIT_BUTTON_TEXT, const.INCORRECT_COLOR,
                               const.EXIT_BUTTON_CORNERS_RADIUS, on_exit),
        const.ActionButtonSpec(const.BUILD_BUTTON_TEXT, const.CORRECT_COLOR,
                               const.BUILD_BUTTON_CORNERS_RADIUS, on_build),
    )

    button_width = (width - 2 * const.BUTTONS_CONTAINER_PADDING -
                    const.BUTTONS_CONTAINER_SPACE_BETWEEN) // 2
    for spec in specs:
        buttons_container.add_children(
            create_button_with_text(
                button_width, const.BUTTON_HEIGHT, spec.color, spec.text,
                corners_radius=spec.corners_radius,
                font_size=const.ACTION_BUTTON_FONT_SIZE, action=spec.action,
            )
        )
    return buttons_container


def _on_build(m_input: TextInput, ef_input: TextInput) -> None:

    max_neighbors = m_input.get_text()
    max_candidates = ef_input.get_text()
    if not max_neighbors.isdigit() or not max_candidates.isdigit():
        return

    loading_menu = loading_menu_setup(int(max_neighbors),
                                      int(max_candidates))

    hnsw_customization_menu.close()
    loading_menu.open()


def hnsw_customization_menu_setup() -> Window:
    base_layer = hnsw_customization_menu.add_layer()
    body_color = BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN)
    card_color = BASE_COLOR.lightened(const.CARD_COLOR_LIGHTEN)

    header = build_header(WINDOW_WIDTH)
    body = FlexBox(WINDOW_WIDTH, const.BODY_HEIGHT, padding=const.BODY_PADDING,
                   space_between=const.BODY_SPACE_BETWEEN, color=body_color)

    content_width = int(WINDOW_WIDTH * const.WELCOME_MESSAGE_WIDTH_RATIO)
    welcome_message = _build_welcome_message(
        content_width, const.BODY_HEIGHT // const.WELCOME_MESSAGE_HEIGHT_RATIO, card_color,
    )
    inputs_container, m_input, ef_construction_input = _build_input_container()

    def _exit():
        hnsw_customization_menu.close()
        sys.exit()

    buttons_container = _build_buttons_container(
        const.BUTTONS_CONTAINER_WIDTH, BASE_COLOR,
        lambda: _on_build(m_input, ef_construction_input),
        _exit,
    )

    body.add_children([welcome_message, inputs_container, buttons_container])
    base_layer.add_children([header, body])
    return hnsw_customization_menu
