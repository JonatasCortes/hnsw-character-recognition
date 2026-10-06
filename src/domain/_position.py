from typing import Self
import numpy as np


class Position(int):

    def __new__(cls, image: np.ndarray, image_sections: int, luminance_threshold: int) -> Self:
        return super().__new__(cls, cls.__calculate(image, image_sections, luminance_threshold))

    @classmethod
    def __calculate(cls, image: np.ndarray, image_sections: int, luminance_threshold: int) -> int:
        binary = image > luminance_threshold
        cropped_binary = cls.__crop_to_content(binary)
        normalized = cls.__normalize_shape(cropped_binary,
                                           (image_sections, image_sections))
        bit_text = (normalized.ravel().astype(
            np.uint8) + 48).tobytes().decode("ascii")
        return int("1" + bit_text, 2)

    @staticmethod
    def __crop_to_content(binary: np.ndarray) -> np.ndarray:
        rows_with_content = np.any(binary, axis=1)
        cols_with_content = np.any(binary, axis=0)

        if not rows_with_content.any():
            return binary

        top, bottom = np.where(rows_with_content)[0][[0, -1]]
        left, right = np.where(cols_with_content)[0][[0, -1]]

        return binary[top:bottom + 1, left:right + 1]

    @staticmethod
    def __normalize_shape(image: np.ndarray, target_shape: tuple[int, int]) -> np.ndarray:
        target_h, target_w = target_shape
        src_h: int
        src_w: int
        src_h, src_w = image.shape

        row_indices = np.linspace(0, src_h - 1, target_h).astype(int)
        col_indices = np.linspace(0, src_w - 1, target_w).astype(int)

        return image[row_indices[:, None], col_indices]
