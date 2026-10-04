from typing import Any, NamedTuple


class Node(dict[str, Any]):
    pass


class Layer(dict[int, Node]):
    pass


class HNSW(dict[int, Layer]):
    pass


class Candidate(NamedTuple):
    distance_to_target: int
    id: int
    position: int
