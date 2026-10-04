import json
from functools import partial
from typing import Callable, Final

from . import _constants as const
from desklab import Button, FlexBox, Text, Window
from interface._utils import create_button_with_text, toggle_brightness_up
from interface._constants import WINDOW_WIDTH, BASE_COLOR, DEFAULT_FONT, DEFAULT_TEST_RESULTS_PATH


confusion_matrix_menu: Final[Window] = Window()

assert len(const.CLASS_LABELS) == const.NUM_CLASSES, (
    "NUM_CLASSES em _constants.py não bate com a quantidade real de classes de Label"
)


def _empty_matrix() -> list[list[int]]:
    return [[0] * const.NUM_COLUMNS for _ in range(const.NUM_CLASSES)]


def _load_confusion_data() -> list[list[int]]:
    try:
        with DEFAULT_TEST_RESULTS_PATH.open(mode="r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return _empty_matrix()

    index = {label: index for index,
             label in enumerate(const.CLASS_LABELS)}
    matrix = _empty_matrix()

    for entry in data.get("confusion_matrix", []):
        expected, actual, count = entry["expected"], entry["actual"], entry["count"]
        if expected in index and actual in index:
            matrix[index[expected]][index[actual]] = count

    return matrix


def _lerp_color(start: tuple[int, int, int], end: tuple[int, int, int], t: float) -> tuple[int, ...]:
    t = max(0.0, min(1.0, t))
    return tuple(round(s + (e - s) * t) for s, e in zip(start, end))


def _row_color(value: int, row_max: int) -> tuple[int, ...]:
    if value <= 0 or row_max <= 0:
        return const.MATRIX_ZERO_CELL_COLOR
    return _lerp_color(const.MATRIX_ZERO_CELL_COLOR, const.MATRIX_MAX_CELL_COLOR, value / row_max)


def _build_cell_modal(modal_layer: FlexBox, close_modal: Callable[[], None]) -> Callable[[str, str, int], None]:
    modal_background = FlexBox(
        const.CELL_MODAL_WIDTH, const.CELL_MODAL_HEIGHT,
        padding=const.CELL_MODAL_PADDING,
        space_between=const.CELL_MODAL_SPACE_BETWEEN,
        corners_radius=const.CELL_MODAL_CORNERS_RADIUS,
        color=BASE_COLOR.lightened(const.MODAL_BACKGROUND_COLOR_LIGHTEN),
    )
    modal_layer.add_children(modal_background)

    title_text = Text("", DEFAULT_FONT.copy(
        size=const.CELL_MODAL_TITLE_FONT_SIZE), "WHITE")
    count_text = Text("", DEFAULT_FONT.copy(
        size=const.CELL_MODAL_TEXT_FONT_SIZE), "WHITE")

    close_button = create_button_with_text(
        const.CELL_MODAL_CLOSE_BUTTON_WIDTH, const.CELL_MODAL_CLOSE_BUTTON_HEIGHT,
        const.CLOSE_BUTTON_COLOR, "X",
        corners_radius=const.CELL_MODAL_CLOSE_BUTTON_CORNERS_RADIUS,
        action=close_modal,
    )

    modal_background.add_children([title_text, count_text, close_button])

    def open_cell_modal(row_label: str, column_label: str, count: int) -> None:
        title_text.set_text(f"{row_label} >> {column_label}")
        count_text.set_text(f"{count} ocorrencia{'s' if count != 1 else ''}")
        modal_layer.set_visibility(True)

    return open_cell_modal


def _build_row_label_cell(text: str, row_height: int) -> FlexBox:
    cell = FlexBox(
        const.MATRIX_LABEL_COLUMN_WIDTH, row_height,
        flex_direction="ROW", horizontal_alignment="CENTER", color=BASE_COLOR,
        bounded=False
    )
    cell.add_children(
        Text(text, DEFAULT_FONT.copy(size=const.MATRIX_LABEL_FONT_SIZE),
             const.MATRIX_LABEL_TEXT_COLOR)
    )
    return cell


def _build_matrix_row(
    row_label: str,
    row_values: list[int],
    row_height: int,
    background: tuple[int, ...],
    open_cell_modal: Callable[[str, str, int], None],
) -> FlexBox:
    row = FlexBox(
        const.MATRIX_GRID_WIDTH, row_height,
        flex_direction="ROW", color=background,
    )
    row.add_children(_build_row_label_cell(row_label, row_height))

    row_max = max(row_values, default=0)

    for column_label, column_width, value in zip(const.CLASS_LABELS, const.COLUMN_WIDTHS, row_values):
        cell = Button(
            column_width, row_height,
            partial(open_cell_modal, row_label, column_label, value),
            corners_radius=const.MATRIX_CELL_CORNERS_RADIUS,
            color=_row_color(value, row_max),
            trigger_actions_on_release=True,
        )
        toggle_brightness_up(cell, const.CELL_BRIGHTNESS_ON_HOVER)
        row.add_children(cell)

    return row


def _build_column_header_row(on_close: Callable[[], None]) -> FlexBox:
    header_row = FlexBox(
        const.MATRIX_GRID_WIDTH, const.MATRIX_HEADER_ROW_HEIGHT,
        flex_direction="ROW", color=BASE_COLOR,
    )

    close_button = create_button_with_text(
        const.CLOSE_BUTTON_WIDTH, const.CLOSE_BUTTON_HEIGHT,
        const.CLOSE_BUTTON_COLOR, const.CLOSE_BUTTON_TEXT,
        corners_radius=const.CLOSE_BUTTON_CORNERS_RADIUS,
        font_size=const.CLOSE_BUTTON_FONT_SIZE, action=on_close,
    )
    header_row.add_children(close_button)

    for label, column_width in zip(const.CLASS_LABELS, const.COLUMN_WIDTHS):
        header_cell = FlexBox(
            column_width, const.MATRIX_HEADER_ROW_HEIGHT,
            flex_direction="ROW", horizontal_alignment="CENTER", color=BASE_COLOR,
            bounded=False
        )
        header_cell.add_children(
            Text(label, DEFAULT_FONT.copy(
                size=const.MATRIX_LABEL_FONT_SIZE), const.MATRIX_LABEL_TEXT_COLOR)
        )
        header_row.add_children(header_cell)

    return header_row


def _build_matrix_panel(
    matrix: list[list[int]],
    open_cell_modal: Callable[[str, str, int], None],
    on_close: Callable[[], None],
) -> FlexBox:

    background_color = BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN)

    panel = FlexBox(
        const.MATRIX_PANEL_WIDTH, const.MATRIX_PANEL_HEIGHT,
        padding=const.MATRIX_PANEL_PADDING,
        corners_radius=const.MATRIX_PANEL_CORNERS_RADIUS,
        color=background_color,
    )

    panel.add_children(_build_column_header_row(on_close))

    for row_label, row_height, row_values in zip(const.CLASS_LABELS, const.ROW_HEIGHTS, matrix):
        panel.add_children(_build_matrix_row(
            row_label, row_values, row_height, background_color.get_tuple(), open_cell_modal))

    return panel


def confusion_matrix_menu_setup() -> Window:
    base_layer = confusion_matrix_menu.add_layer()
    cell_modal_layer = confusion_matrix_menu.add_layer(
        color=const.MODAL_OVERLAY_COLOR, visible=False)

    def close_cell_modal() -> None:
        cell_modal_layer.set_visibility(False)

    body_background = BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN)
    body = FlexBox(
        WINDOW_WIDTH, const.BODY_HEIGHT,
        padding=const.BODY_PADDING, space_between=const.BODY_SPACE_BETWEEN,
        color=body_background,
    )

    matrix = _load_confusion_data()
    open_cell_modal = _build_cell_modal(cell_modal_layer, close_cell_modal)

    body.add_children(
        _build_matrix_panel(matrix, open_cell_modal,
                            confusion_matrix_menu.close)
    )
    base_layer.add_children(body)

    return confusion_matrix_menu
