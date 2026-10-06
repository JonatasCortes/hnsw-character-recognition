from collections.abc import Callable
from typing import Final

import numpy as np
from desklab import Color, DrawingArea, FlexBox, Listener, Text, Window

from interface._constants import BASE_COLOR, WINDOW_WIDTH
from interface._utils import (build_header, create_button_with_image,
                              create_button_with_text)
from src.hnsw import Hnsw

from . import _constants as const

classify_menu: Final[Window] = Window()


def _build_toolbar(drawing_area: DrawingArea) -> FlexBox:
    color = BASE_COLOR.lightened(const.TOOLBAR_LIGHTEN)
    toolbar = FlexBox(WINDOW_WIDTH, const.TOOLBAR_HEIGHT, (0, 0, 0, 240),
                      const.TOOLBAR_SPACE_BETWEEN, "ROW", "LEFT", color=color)

    tool_actions = (drawing_area.draw, drawing_area.erase, drawing_area.clear)
    toolbar.add_children([
        create_button_with_image(f"{const.ASSETS_PATH}{icon}",
                                 const.TOOL_BUTTON_SIZE, const.TOOL_BUTTON_SIZE,
                                 color, action)
        for icon, action in zip(const.TOOL_ICONS, tool_actions)
    ])
    return toolbar


def _build_side_panel(classification_text: Text,
                      on_return: Callable[[], None]) -> FlexBox:
    panel = FlexBox(const.PANEL_WIDTH, const.BODY_HEIGHT, const.PANEL_PADDING,
                    const.PANEL_SPACE_BETWEEN,
                    color=BASE_COLOR.lightened(const.PANEL_LIGHTEN))

    display = FlexBox(const.PANEL_CONTENT_WIDTH, const.DISPLAY_HEIGHT,
                      corners_radius=const.DISPLAY_CORNERS_RADIUS,
                      color=BASE_COLOR.lightened(const.DISPLAY_LIGHTEN))
    display.add_children(classification_text)

    return_button = create_button_with_text(
        const.PANEL_CONTENT_WIDTH, const.RETURN_BUTTON_HEIGHT,
        const.RETURN_COLOR, const.RETURN_BUTTON_TEXT,
        corners_radius=const.RETURN_BUTTON_CORNERS_RADIUS, action=on_return,
    )

    panel.add_children([display, return_button])
    return panel


def _read_canvas(drawing_area: DrawingArea) -> np.ndarray:
    pixels = np.frombuffer(drawing_area.get_canvas_buffer(), dtype=np.uint8)
    rgb_image = pixels.reshape(drawing_area.get_height(),
                               drawing_area.get_width(), 3)
    return np.mean(rgb_image, axis=2).astype(np.uint8)


def _make_classifier(drawing_area: DrawingArea, hnsw: Hnsw,
                     classification_text: Text) -> Callable[[], None]:
    last_image: np.ndarray | None = None

    def update_classification() -> None:
        nonlocal last_image
        image = _read_canvas(drawing_area)
        if last_image is not None and np.array_equal(image, last_image):
            return
        last_image = image
        if image.any():
            classification_text.set_text(hnsw.classify(image))
        else:
            classification_text.set_text(const.DISPLAY_DEFAULT_TEXT)

    return update_classification


def classify_menu_setup(hnsw: Hnsw) -> Window:
    drawing_area = DrawingArea(const.CANVAS_WIDTH, const.BODY_HEIGHT, 0,
                               Color(const.CANVAS_COLOR),
                               eraser_width=const.ERASER_WIDTH,
                               brush_width=const.BRUSH_WIDTH)
    drawing_area.set_brush_color(const.BRUSH_COLOR)

    classification_text = Text(const.DISPLAY_DEFAULT_TEXT, const.DISPLAY_FONT,
                               "WHITE")
    side_panel = _build_side_panel(classification_text, classify_menu.close)

    classify_listener = Listener(
        lambda: True,
        _make_classifier(drawing_area, hnsw, classification_text),
    )

    body = FlexBox(WINDOW_WIDTH, const.BODY_HEIGHT, flex_direction="ROW")
    body.add_children([drawing_area, side_panel, classify_listener])

    base_layer = classify_menu.add_layer()
    base_layer.add_children([build_header(WINDOW_WIDTH),
                             _build_toolbar(drawing_area), body])
    return classify_menu
