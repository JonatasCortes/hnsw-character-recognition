from src.domain import HNSW, Node, Layer, Candidate, Position
from src.services._heuristic import SelectionHeuristic
from src.services._search_engine import SearchEngine
from src.services._connection_manager import ConnectionManager
from src.services._distance_metric import hamming_distance
from random import random
import math
import numpy as np


class NodeManager:

    def __init__(self, hnsw: HNSW, max_neighbors: int, max_candidates: int, image_sections: int, luminance_threshold: int) -> None:
        self.__hnsw = hnsw
        self.__max_neighbors = max_neighbors
        self.__max_candidates = max_candidates
        self.__image_sections = image_sections
        self.__luminance_threshold = luminance_threshold
        self.__hnsw_max_layer_id = -1
        self.__entry_point_id: int | None = None

        self.__heuristic = SelectionHeuristic(hnsw, hamming_distance)
        self.__search_engine = SearchEngine(hnsw, hamming_distance)
        self.__connection_manager = ConnectionManager(hnsw)

    def insert(self, target_id: int, image: np.ndarray, label: int) -> None:
        position = Position(image, self.__image_sections,
                            self.__luminance_threshold)
        top_layer = self.__determine_insertion_layer()
        self.__register_node_in_layers(target_id, position,
                                       int(label), top_layer)
        if self.__entry_point_id is None:
            self.__hnsw_max_layer_id = top_layer
            self.__entry_point_id = target_id
            return

        entry_node_id = self.__descend_to_insertion_layer(position, top_layer)
        self.__connect_node(target_id, position, top_layer, entry_node_id)
        self.__promote_entry_point_if_needed(target_id, top_layer)

    def __determine_insertion_layer(self) -> int:
        r = random()
        r = r if r != 0 else 0.1
        raw_layer = -math.log(r) * (1.0 / math.log(self.__max_neighbors))
        return math.floor(raw_layer)

    def __register_node_in_layers(self, target_id: int, position: Position, label: int, top_layer: int) -> None:
        for layer_id in range(top_layer + 1):
            if layer_id not in self.__hnsw:
                self.__hnsw[layer_id] = Layer()
            self.__hnsw[layer_id][target_id] = Node({
                "position": position,
                "label": label,
                "neighbors": []
            })

    def __descend_to_insertion_layer(self, target_position: Position, top_layer: int) -> int:
        entry_node_id = self.__entry_point_id
        assert isinstance(entry_node_id, int)

        for layer_id in range(self.__hnsw_max_layer_id, top_layer, -1):
            self.__search_engine.explore_layer(target_position, layer_id, 1,
                                               entry_node_id)
            entry_node_id = self.__search_engine.get_nearest_neighbor()

        return entry_node_id

    def __connect_node(self, target_id: int, target_position: Position, top_layer: int, entry_node_id: int) -> None:
        connect_start_layer = min(top_layer, self.__hnsw_max_layer_id)

        for layer_id in range(connect_start_layer, -1, -1):
            max_candidates = self.__max_candidates * \
                (2 if layer_id == 0 else 1)
            max_neighbors = self.__max_neighbors * (2 if layer_id == 0 else 1)

            self.__search_engine.explore_layer(target_position, layer_id,
                                               max_candidates, entry_node_id)
            entry_node_id = self.__search_engine.get_nearest_neighbor()

            candidates = self.__search_engine.get_candidates()
            selected_neighbors = self.__heuristic.select_best(candidates, layer_id,
                                                              max_neighbors)
            self.__connection_manager.update_connections(target_id, layer_id,
                                                         selected_neighbors)

            for neighbor in selected_neighbors:
                self.__prune_if_overflowing(neighbor.id, layer_id,
                                            max_neighbors)

    def __prune_if_overflowing(self, node_id: int, layer_id: int, max_neighbors: int) -> None:
        layer = self.__hnsw[layer_id]
        node = layer[node_id]
        neighbor_ids: list[int] = node["neighbors"]
        excess = len(neighbor_ids) - max_neighbors

        if excess <= 0:
            return

        base_position = node["position"]

        if excess == 1:
            farthest_id = max(
                neighbor_ids,
                key=lambda neighbor_id: hamming_distance(
                    layer[neighbor_id]["position"], base_position),
            )
            neighbor_ids.remove(farthest_id)
            layer[farthest_id]["neighbors"].remove(node_id)
            return

        candidates = self.__build_candidates(neighbor_ids, base_position,
                                             layer_id)
        worst_neighbors = self.__heuristic.select_worst(candidates, layer_id,
                                                        excess)
        self.__connection_manager.prune_connections(node_id, layer_id,
                                                    worst_neighbors)

    def __build_candidates(self, neighbor_ids: list[int], base_position: Position, layer_id: int) -> list[Candidate]:
        layer = self.__hnsw[layer_id]
        candidates: list[Candidate] = []

        for neighbor_id in neighbor_ids:
            neighbor_position = layer[neighbor_id]["position"]
            distance = hamming_distance(neighbor_position,
                                        base_position)
            candidate = Candidate(neighbor_id, neighbor_position, distance)
            candidates.append(candidate)

        return candidates

    def __promote_entry_point_if_needed(self, target_id: int, top_layer: int) -> None:
        if top_layer > self.__hnsw_max_layer_id:
            self.__hnsw_max_layer_id = top_layer
            self.__entry_point_id = target_id
