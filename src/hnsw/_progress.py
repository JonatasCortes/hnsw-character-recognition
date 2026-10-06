from typing import Callable

ProgressCallback = Callable[[float], None]


class ProgressTracker:

    def __init__(self) -> None:
        self.__value = 0.0
        self.__done = False

    def reset(self) -> None:
        self.__value = 0.0
        self.__done = False

    def update(self, value: float) -> None:
        self.__value = value

    def finish(self) -> None:
        self.__value = 100.0
        self.__done = True

    def get_value(self) -> float:
        return self.__value

    def is_done(self) -> bool:
        return self.__done
