from src.domain import Candidate
from typing import Callable
from src.domain import HNSW
import heapq


class SearchEngine:

    def __init__(self, hnsw: HNSW, distance_metric: Callable[[int, int], int]) -> None:
        self.__hnsw = hnsw
        self.__distance_metric = distance_metric
        self.__nearest_neighbor: int | None = None
        self.__candidates: list[Candidate] = []

    def get_candidates(self) -> list[Candidate]:
        return self.__candidates

    def get_nearest_neighbor(self) -> int:
        if self.__nearest_neighbor is None:
            raise RuntimeError("No layer was explored yet.")
        return self.__nearest_neighbor

    def explore_layer(self, target_position: int, layer_id: int, max_candidates: int, entry_node_id: int = 0) -> None:
        layer = self.__hnsw[layer_id]
        distance_metric = self.__distance_metric
        push, pop, replace = heapq.heappush, heapq.heappop, heapq.heapreplace

        entry_distance = distance_metric(
            layer[entry_node_id]["position"], target_position)
        frontier: list[tuple[int, int]] = [(entry_distance,
                                            entry_node_id)]

        best: list[tuple[int, int]] = [(-entry_distance, entry_node_id)]
        visited: set[int] = {entry_node_id}

        while frontier:
            distance, node_id = pop(frontier)

            if len(best) >= max_candidates and distance > -best[0][0]:
                break

            for neighbor_id in layer[node_id]["neighbors"]:
                if neighbor_id in visited:
                    continue
                visited.add(neighbor_id)

                neighbor_distance = distance_metric(
                    layer[neighbor_id]["position"], target_position)

                if len(best) < max_candidates:
                    push(best, (-neighbor_distance, neighbor_id))
                elif neighbor_distance < -best[0][0]:
                    replace(best, (-neighbor_distance, neighbor_id))
                else:
                    continue
                push(frontier, (neighbor_distance, neighbor_id))

        self.__candidates = [
            Candidate(-d, i, layer[i]["position"]) for d, i in best]
        self.__nearest_neighbor = max(best)[1]
