from . import _constants as const
from typing import Any, Callable, Final
from desklab import FlexBox, Window
from interface._utils import create_button_with_text, build_header
from interface._constants import WINDOW_WIDTH, BASE_COLOR

main_menu: Final[Window] = Window()


def _build_buttons_container(width: int, height: int, actions: list[Callable[[], Any]]) -> FlexBox:
    container = FlexBox(width, height, space_between=const.BUTTONS_CONTAINER_SPACE_BETWEEN,
                        corners_radius=const.BUTTONS_CONTAINER_CORNERS_RADIUS, color=BASE_COLOR)

    button_width = int(width / const.ACTION_BUTTON_WIDTH_RATIO)
    button_height = int(height / const.ACTION_BUTTON_HEIGHT_RATIO)

    a1, a2, a3 = actions

    specs: tuple[const.ActionButtonSpec, ...] = (
        const.ActionButtonSpec(const.START_BUTTON_TEXT, const.START_BUTTON_CORNERS_RADIUS,
                               const.START_BUTTON_COLOR, a1),
        const.ActionButtonSpec(const.METRICS_BUTTON_TEXT, const.METRICS_BUTTON_CORNERS_RADIUS,
                               const.METRICS_BUTTON_COLOR, a2),
        const.ActionButtonSpec(const.EXIT_BUTTON_TEXT, const.EXIT_BUTTON_CORNERS_RADIUS,
                               const.EXIT_BUTTON_COLOR, a3),
    )

    for spec in specs:
        container.add_children(
            create_button_with_text(
                button_width,
                button_height,
                spec.color,
                spec.text,
                corners_radius=spec.corners_radius,
                font_size=const.ACTION_BUTTON_FONT_SIZE,
                action=spec.action,
            )
        )

    return container


def main_menu_setup(classify_menu: Window, metrics_menu: Window) -> Window:
    base_layer = main_menu.add_layer()

    header = build_header(WINDOW_WIDTH)
    body = FlexBox(WINDOW_WIDTH, const.BODY_HEIGHT,
                   color=BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN))

    buttons_actions: list[Callable[[], Any]] = [
        classify_menu.open,
        metrics_menu.open,
        main_menu.close
    ]

    buttons_container = _build_buttons_container(
        const.BUTTONS_CONTAINER_WIDTH,
        const.BUTTONS_CONTAINER_HEIGHT,
        buttons_actions,
    )
    body.add_children(buttons_container)

    base_layer.add_children([header, body])
    return main_menu
