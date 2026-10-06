from threading import Thread
from typing import Callable, Final

from . import _constants as const
from desklab import FlexBox, Window, RectangularArea, Listener, Text
from interface._utils import build_header
from interface._constants import (
    WINDOW_WIDTH,
    BASE_COLOR,
    DEFAULT_FONT,
    DEFAULT_DATABASE_PATH,
    DEFAULT_TEST_RESULTS_PATH,
)

from src.hnsw import Hnsw, HnswParameters


loading_menu: Final[Window] = Window()


class _ProgressRenderer:

    def __init__(
        self,
        container: FlexBox,
        get_progress: Callable[[], float],
        label: str,
        bar_color: str,
    ) -> None:
        self.__container = container
        self.__get_progress = get_progress
        self.__label = label
        self.__bar_color = bar_color
        self.__rendered_progress: float | None = None

    def has_changed(self) -> bool:
        return round(self.__get_progress(), 2) != self.__rendered_progress

    def render(self) -> None:
        progress = round(self.__get_progress(), 2)
        self.__rendered_progress = progress

        progress_text = Text(
            f"{self.__label}: {progress:.2f}%",
            DEFAULT_FONT,
            const.PROGRESS_TEXT_COLOR,
        )

        bar_background = FlexBox(
            self.__container.get_width() - const.PROGRESS_BAR_HORIZONTAL_MARGIN,
            const.PROGRESS_BAR_HEIGHT,
            color=BASE_COLOR.darkened(const.PROGRESS_BAR_BACKGROUND_DARKEN),
            corners_radius=const.PROGRESS_BAR_BACKGROUND_CORNER_RADIUS,
            horizontal_alignment=const.PROGRESS_BAAR_HORIZONTAL_ALIGNMENT,
        )

        filled_width = round(bar_background.get_width() * (progress / 100))

        if filled_width > 0:
            bar_background.add_children([
                RectangularArea(
                    filled_width,
                    const.PROGRESS_BAR_HEIGHT,
                    self.__bar_color,
                    const.PROGRESS_BAR_CORNER_RADIUS,
                )
            ])

        self.__container.clear_children()
        self.__container.add_children([progress_text, bar_background])


def _build_progress_container() -> FlexBox:
    return FlexBox(
        WINDOW_WIDTH - const.PROGRESS_CONTAINER_HORIZONTAL_MARGIN,
        const.PROGRESS_CONTAINER_HEIGHT,
        space_between=const.PROGRESS_CONTAINER_SPACE_BETWEEN,
        corners_radius=const.PROGRESS_CONTAINER_CORNER_RADIUS,
        color=BASE_COLOR,
        padding=const.PROGRESS_CONTAINER_PADDING,
        horizontal_alignment=const.PROGRESS_CONTAINER_HORIZONTAL_ALIGNMENT,
    )


def _build_progress_section(
    container: FlexBox,
    get_progress: Callable[[], float],
    label: str,
    bar_color: str,
    start_condition: Callable[[], bool],
    start_action: Callable[[], object],
) -> tuple[Listener, Listener]:
    renderer = _ProgressRenderer(container, get_progress, label, bar_color)

    begin_listener = Listener(
        start_condition,
        lambda: Thread(target=start_action, daemon=True).start(),
        listen_once=True,
    )

    progress_listener = Listener(renderer.has_changed, renderer.render)

    return begin_listener, progress_listener


def loading_menu_setup(parameters: HnswParameters) -> Window:

    hnsw = Hnsw(parameters, DEFAULT_DATABASE_PATH, DEFAULT_TEST_RESULTS_PATH)

    base_layer = loading_menu.add_layer()

    header = build_header(WINDOW_WIDTH)

    body = FlexBox(
        WINDOW_WIDTH,
        const.BODY_HEIGHT,
        color=BASE_COLOR.lightened(const.BODY_COLOR_LIGHTEN),
        space_between=const.BODY_SPACE_BETWEEN,
    )

    training_container = _build_progress_container()
    testing_container = training_container.copy()

    begin_training, training_progress_bar = _build_progress_section(
        training_container,
        hnsw.get_train_progress,
        "Training",
        const.TRAINING_BAR_COLOR,
        lambda: True,
        hnsw.train,
    )

    begin_testing, testing_progress_bar = _build_progress_section(
        testing_container,
        hnsw.get_test_progress,
        "Testing",
        const.TESTING_BAR_COLOR,
        hnsw.is_train_done,
        hnsw.test,
    )

    progress_finished = Listener(
        hnsw.is_test_done,
        loading_menu.close,
        listen_once=True
    )

    body.add_children(
        [
            begin_training,
            training_progress_bar,
            training_container,
            begin_testing,
            testing_progress_bar,
            testing_container,
            progress_finished,
        ]
    )

    base_layer.add_children([header, body])
    return loading_menu
