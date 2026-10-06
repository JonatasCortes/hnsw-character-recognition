from src.domain import HNSW, Candidate


class ConnectionManager:

    def __init__(self, hnsw: HNSW) -> None:
        self.__hnsw = hnsw

    def update_connections(self, node_id: int, layer_id: int, new_neighbors: list[Candidate]):
        layer = self.__hnsw[layer_id]
        node = layer[node_id]
        node["neighbors"] = []

        for neighbor in new_neighbors:
            node["neighbors"].append(neighbor.id)
            neighbor_data = layer[neighbor.id]
            neighbor_data["neighbors"].append(node_id)

    def prune_connections(self, node_id: int, layer_id: int, removed_neighbors: list[Candidate]):
        layer = self.__hnsw[layer_id]
        node = layer[node_id]

        for neighbor in removed_neighbors:
            node["neighbors"].remove(neighbor.id)
            neighbor_data = layer[neighbor.id]
            neighbor_data["neighbors"].remove(node_id)
