import json
from pathlib import Path
from typing import Any

from src.domain import HNSW
from src.hnsw._parameters import HnswParameters
from src.hnsw._tester import HnswTestReport


class HnswStorage:

    def save_model(self, file_path: Path, parameters: HnswParameters, hnsw: HNSW) -> None:
        content: dict[str, Any] = {
            "parameters": parameters.to_dict(),
            "layers": hnsw
        }
        with file_path.open(mode="w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, separators=(",", ":"))

    def load_model(self, file_path: Path) -> tuple[dict[str, Any], HNSW]:
        with file_path.open(mode="r", encoding="utf-8") as file:
            content = json.load(file, object_hook=self.__restore_integer_keys)
        return content["parameters"], HNSW(content["layers"])

    def save_report(self, file_path: Path, parameters: HnswParameters, report: HnswTestReport) -> None:
        content: dict[str, Any] = {
            "parameters": parameters.to_dict(),
            "total_tests": report.total_tests,
            "total_correct": report.total_correct,
            "total_incorrect": report.total_incorrect,
            "accuracy": report.accuracy,
            "execution_time_per_test": report.execution_time_per_test,
            "total_execution_time": report.total_execution_time,
            "confusion_matrix": [
                {
                    "expected": expected,
                    "actual": actual,
                    "count": count
                }
                for (expected, actual), count in report.confusion_counts.items()
            ],
        }
        with file_path.open(mode="w", encoding="utf-8") as file:
            json.dump(content, file, indent=4, ensure_ascii=False)

    @staticmethod
    def __restore_integer_keys(obj: dict[Any, Any]) -> dict[Any, Any]:
        if obj and all(key.isdigit() for key in obj):
            return {int(key): value for key, value in obj.items()}
        return obj
