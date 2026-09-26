from threading import Thread
from typing import Final, Protocol, Callable

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

from src.hnsw import HnswBuilder, HnswTester


class Progress(Protocol):

    def get_progress(self) -> float:
        ...


loading_menu: Final[Window] = Window()


def _update_progress(
    progress_container: FlexBox,
    progress_provider: Progress,
    label: str,
    bar_color: str,
) -> None:
    progress_container.clear_children()

    progress = progress_provider.get_progress()

    progress_text = Text(
        f"{label}: {progress:.2f}%",
        DEFAULT_FONT,
        const.PROGRESS_TEXT_COLOR,
    )

    bar_background = FlexBox(
        progress_container.get_width() - const.PROGRESS_BAR_HORIZONTAL_MARGIN,
        const.PROGRESS_BAR_HEIGHT,
        color=BASE_COLOR.darkened(const.PROGRESS_BAR_BACKGROUND_DARKEN),
        corners_radius=const.PROGRESS_BAR_BACKGROUND_CORNER_RADIUS,
        horizontal_alignment=const.PROGRESS_BAAR_HORIZONTAL_ALIGNMENT
    )

    filled_width = round(bar_background.get_width() * (progress / 100))

    progress_bar = RectangularArea(
        filled_width,
        const.PROGRESS_BAR_HEIGHT,
        bar_color,
        const.PROGRESS_BAR_CORNER_RADIUS,
    )

    bar_background.add_children([progress_bar])
    progress_container.add_children([progress_text, bar_background])


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
    provider: Progress,
    label: str,
    bar_color: str,
    start_condition: Callable[[], bool],
    start_action: Callable[[], None],
) -> tuple[Listener, Listener]:
    begin_listener = Listener(
        start_condition,
        lambda: Thread(target=start_action, daemon=True).start(),
        listen_once=True,
    )

    progress_listener = Listener(
        lambda: True,
        lambda: _update_progress(container, provider, label, bar_color),
    )

    return begin_listener, progress_listener


def loading_menu_setup(max_neighbors: int, max_candidates: int) -> Window:
    hnsw_builder = HnswBuilder(
        DEFAULT_DATABASE_PATH,
        max_neighbors,
        max_candidates,
    )

    hnsw_tester = HnswTester(
        DEFAULT_DATABASE_PATH,
        DEFAULT_TEST_RESULTS_PATH,
        max_candidates,
    )

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
        hnsw_builder,
        "Training",
        const.TRAINING_BAR_COLOR,
        lambda: True,
        hnsw_builder.build,
    )

    begin_testing, testing_progress_bar = _build_progress_section(
        testing_container,
        hnsw_tester,
        "Testing",
        const.TESTING_BAR_COLOR,
        hnsw_builder.is_done,
        hnsw_tester.run,
    )

    progress_finished = Listener(
        hnsw_tester.is_done,
        loading_menu.close,
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
