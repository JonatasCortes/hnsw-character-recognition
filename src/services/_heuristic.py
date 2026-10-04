from enum import Enum
from typing import Callable
from src.domain import HNSW, Candidate


class SelectionHeuristic:

    class _SelectionMetric(Enum):
        BEST = 1
        WORST = 0

    def __init__(self, hnsw: HNSW, distance_metric: Callable[[int, int], int]) -> None:
        self.__hnsw = hnsw
        self.__distance_metric = distance_metric

    def select_best(self, candidates: list[Candidate], layer_id: int,  max_selected: int) -> list[Candidate]:
        return self.__select_candidates(candidates, layer_id, max_selected, self._SelectionMetric.BEST)

    def select_worst(self, candidates: list[Candidate], layer_id: int, max_selected: int) -> list[Candidate]:
        return self.__select_candidates(candidates, layer_id, max_selected, self._SelectionMetric.WORST)

    def __select_candidates(self, candidates: list[Candidate], layer_id: int, max_selected: int, selection_metric: _SelectionMetric) -> list[Candidate]:

        is_worst_selection = selection_metric == self._SelectionMetric.WORST
        candidates.sort(reverse=is_worst_selection)
        selected: list[Candidate] = []

        for candidate in candidates:
            if self.__is_good_candidate(candidate, selected):
                selected.append(candidate)
            if len(selected) == max_selected:
                break

        return selected

    def __is_good_candidate(self, candidate: Candidate, selected: list[Candidate]) -> bool:
        for previous in selected:
            distance_to_previous = self.__distance_metric(
                candidate.position, previous.position)
            if distance_to_previous < candidate.distance_to_target:
                return False
        return True
