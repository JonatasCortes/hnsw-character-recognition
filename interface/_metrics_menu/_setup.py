import json
from typing import Any, Callable, Final
from desklab import Color, FlexBox, Text, Window
from interface._constants import (BASE_COLOR, DEFAULT_FONT,
                                  DEFAULT_TEST_RESULTS_PATH, WINDOW_WIDTH)
from interface._utils import build_header, create_button_with_text
from . import _constants as const
metrics_menu: Final[Window] = Window()


def _load_results() -> dict[str, Any]:
    try:
        with DEFAULT_TEST_RESULTS_PATH.open(mode="r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _format_field(field: const.ResultField, source: dict[str, Any]) -> str:
    value = source.get(field.key)
    if value is None:
        return const.DEFAULT_METRIC_VALUE
    return field.format_value(value)


def _build_half(text: str, font_size: int, width: int,
                color: Color | tuple[int, ...],
                corners_radius: tuple[int, int, int, int],
                horizontal_alignment: str,
                padding: int | tuple[int, ...]) -> FlexBox:
    half = FlexBox(width, const.CARD_HEIGHT, padding,
                   corners_radius=corners_radius,
                   horizontal_alignment=horizontal_alignment,
                   color=color)
    half.add_children(
        Text(text, DEFAULT_FONT.copy(size=font_size), const.TEXT_COLOR))
    return half


def _build_card(field: const.ResultField, source: dict[str, Any]) -> FlexBox:
    value_color = (field.accent_color
                   or BASE_COLOR.lightened(const.VALUE_BOX_COLOR_LIGHTEN))
    card = FlexBox(const.CARD_WIDTH, const.CARD_HEIGHT,
                   0, 0, "ROW", color=BASE_COLOR)
    card.add_children([
        _build_half(field.label, const.LABEL_FONT_SIZE, const.LABEL_BOX_WIDTH,
                    BASE_COLOR.lightened(const.LABEL_BOX_COLOR_LIGHTEN),
                    const.LABEL_BOX_CORNERS_RADIUS, "LEFT", (0, 0, 0, 10)),
        _build_half(_format_field(field, source), const.VALUE_FONT_SIZE,
                    const.VALUE_BOX_WIDTH, value_color,
                    const.VALUE_BOX_CORNERS_RADIUS, "CENTER", 0),
    ])
    return card


def _build_action_row(open_confusion_matrix: Callable[[], None]) -> FlexBox:
    row = FlexBox(const.CARD_WIDTH, const.CARD_HEIGHT, 0,
                  const.CARDS_AREA_SPACE_BETWEEN, "ROW",
                  color=BASE_COLOR)
    row.add_children([
        create_button_with_text(
            const.CONFUSION_MATRIX_BUTTON_WIDTH, const.CARD_HEIGHT,
            const.CONFUSION_MATRIX_BUTTON_COLOR,
            const.CONFUSION_MATRIX_BUTTON_TEXT,
            corners_radius=const.ACTION_BUTTON_CORNERS_RADIUS,
            font_size=const.ACTION_BUTTON_FONT_SIZE,
            action=open_confusion_matrix,
        ),
        create_button_with_text(
            const.RETURN_BUTTON_WIDTH, const.CARD_HEIGHT,
            const.RETURN_BUTTON_COLOR, const.RETURN_BUTTON_TEXT,
            corners_radius=const.ACTION_BUTTON_CORNERS_RADIUS,
            font_size=const.ACTION_BUTTON_FONT_SIZE,
            action=metrics_menu.close,
        ),
    ])
    return row


def _build_container(title: str, rows: list[FlexBox]) -> FlexBox:
    container = FlexBox(const.CONTAINER_WIDTH, const.CONTAINER_HEIGHT,
                        corners_radius=const.CONTAINER_CORNERS_RADIUS,
                        color=BASE_COLOR)

    title_bar = FlexBox(const.CONTAINER_WIDTH, const.TITLE_BAR_HEIGHT,
                        corners_radius=const.TITLE_CORNERS_RADIUS,
                        color=BASE_COLOR.lightened(const.TITLE_BAR_COLOR_LIGHTEN))
    title_bar.add_children(
        Text(title, DEFAULT_FONT.copy(size=const.TITLE_FONT_SIZE),
             const.TEXT_COLOR))

    cards_area = FlexBox(const.CONTAINER_WIDTH, const.CARDS_AREA_HEIGHT,
                         const.CARDS_AREA_PADDING,
                         const.CARDS_AREA_SPACE_BETWEEN,
                         corners_radius=const.CARDS_AREA_CORNERS_RADIUS,
                         color=BASE_COLOR)
    cards_area.add_children(rows)  # type: ignore

    container.add_children([title_bar, cards_area])
    return container


def metrics_menu_setup(confusion_matrix_menu: Window) -> Window:
    results = _load_results()
    parameters: dict[str, Any] = results.get("parameters", {})

    parameter_rows = [_build_card(field, parameters)
                      for field in const.PARAMETER_FIELDS]
    metric_rows = [_build_card(field, results)
                   for field in const.METRIC_FIELDS]
    metric_rows.append(_build_action_row(confusion_matrix_menu.open))

    body = FlexBox(WINDOW_WIDTH, const.BODY_HEIGHT, const.BODY_PADDING,
                   const.CONTAINERS_SPACE_BETWEEN, "ROW",
                   color=BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN))
    body.add_children([
        _build_container(const.PARAMETERS_TITLE, parameter_rows),
        _build_container(const.METRICS_TITLE, metric_rows),
    ])

    base_layer = metrics_menu.add_layer()
    base_layer.add_children([build_header(WINDOW_WIDTH), body])
    return metrics_menu
