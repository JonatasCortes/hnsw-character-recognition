from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class HnswParameters:
    max_neighbors: int
    construction_max_candidates: int
    classification_max_candidates: int
    image_sections: int
    luminance_threshold: int
    layer_growth_factor: float | None = None
    shuffle_seed: int = 0

    @property
    def resolved_layer_growth_factor(self) -> float:
        if self.layer_growth_factor is None:
            return float(self.max_neighbors)
        return self.layer_growth_factor

    def to_dict(self) -> dict[str, Any]:
        values = asdict(self)
        values["layer_growth_factor"] = self.resolved_layer_growth_factor
        return values
