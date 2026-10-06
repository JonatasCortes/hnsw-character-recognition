from bisect import bisect_right
from collections import Counter
from typing import Sequence


class LayerPlanner:

    def __init__(self, growth_factor: float) -> None:
        if growth_factor <= 1:
            raise ValueError("growth_factor must be greater than 1.")
        self.__growth_factor = growth_factor

    def plan(self, labels: Sequence[int]) -> list[int]:
        if len(labels) == 0:
            raise ValueError("labels must not be empty.")

        label_ids = [int(label) for label in labels]
        capacity_by_label = Counter(label_ids)
        sorted_labels = sorted(capacity_by_label)
        capacities = [capacity_by_label[label] for label in sorted_labels]

        layer_sizes = self.__compute_layer_sizes(len(sorted_labels),
                                                 len(label_ids))
        quotas_by_layer = [self.__distribute_evenly(size, capacities)
                           for size in layer_sizes]
        quotas_by_label = dict(zip(sorted_labels, zip(*quotas_by_layer)))

        return self.__assign_layers(label_ids, quotas_by_label,
                                    len(layer_sizes))

    def __compute_layer_sizes(self, label_count: int, total_nodes: int) -> list[int]:
        sizes: list[int] = []
        exponent = 0
        size = label_count

        while size < total_nodes:
            sizes.append(size)
            exponent += 1
            exponential_size = round(
                label_count * self.__growth_factor ** exponent)
            size = max(sizes[-1] + 1, exponential_size)

        sizes.append(total_nodes)
        return sizes

    def __distribute_evenly(self, size: int, capacities: list[int]) -> list[int]:
        level = self.__find_level(size, capacities)
        quotas = [min(capacity, level) for capacity in capacities]
        remainder = size - sum(quotas)

        for index, capacity in enumerate(capacities):
            if remainder == 0:
                break
            if capacity > level:
                quotas[index] += 1
                remainder -= 1

        return quotas

    @staticmethod
    def __find_level(size: int, capacities: list[int]) -> int:
        low, high = 0, max(capacities)

        while low < high:
            middle = (low + high + 1) // 2
            filled = sum(min(capacity, middle) for capacity in capacities)
            if filled <= size:
                low = middle
            else:
                high = middle - 1

        return low

    @staticmethod
    def __assign_layers(label_ids: list[int], quotas_by_label: dict[int, tuple[int, ...]], layer_count: int) -> list[int]:
        occurrences: Counter[int] = Counter()
        top_layers: list[int] = []

        for label in label_ids:
            layer_index = bisect_right(quotas_by_label[label],
                                       occurrences[label])
            occurrences[label] += 1
            top_layers.append(layer_count - 1 - layer_index)

        return top_layers
