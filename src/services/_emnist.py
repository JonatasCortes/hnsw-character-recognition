"""
This module was adapted from the 'emnist' python package,
available at https://github.com/hosford42/EMNIST
"""

import gzip
import logging
import os
import zipfile
import numpy as np
import requests


# =======================================================================
# PUBLIC INTERFACE
# =======================================================================


def extract_balanced_training_images():
    return _extract_data("balanced", "train", "images")


def extract_balanced_testing_images():
    return _extract_data("balanced", "test", "images")


def extract_balanced_training_labels():
    return _extract_data("balanced", "train", "labels")


def extract_balanced_testing_labels():
    return _extract_data("balanced", "test", "labels")


def delete_cached_dataset():
    if os.path.exists(_CACHE_FILE_PATH):
        os.remove(_CACHE_FILE_PATH)


# =======================================================================
# PRIVATE AUXILIAR FUNCTIONS
# =======================================================================


_logger = logging.getLogger(__name__)
_SOURCE_URL = 'https://biometrics.nist.gov/cs_links/EMNIST/gzip.zip'
_CACHE_FILE_PATH = os.path.expanduser('~/.cache/emnist/emnist.zip')
_ZIP_PATH_TEMPLATE = 'gzip/emnist-{dataset}-{usage}-{matrix}-idx{dim}-ubyte.gz'
_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 '
                  'Safari/537.36 Edg/115.0.1901.203'
}


def _extract_data(dataset: str, usage: str, component: str):
    _ensure_cached_data()

    dim = 3 if component == "images" else 1
    zip_internal_path = _ZIP_PATH_TEMPLATE.format(dataset=dataset, usage=usage,
                                                  matrix=component, dim=dim)

    with zipfile.ZipFile(_CACHE_FILE_PATH) as zf:
        compressed_data = zf.read(zip_internal_path)

    data = gzip.decompress(compressed_data)
    array = _parse_idx_file_into_numpy_array(data)

    final_array = array.swapaxes(1, 2) if dim == 3 else array
    return final_array


def _ensure_cached_data():
    if os.path.isfile(_CACHE_FILE_PATH) and os.path.getsize(_CACHE_FILE_PATH) > 0:
        _logger.info(f"Cached file found at {_CACHE_FILE_PATH}.")
        return _CACHE_FILE_PATH

    save_folder = os.path.dirname(_CACHE_FILE_PATH)

    if not os.path.isdir(save_folder):
        _logger.info("Creating folder %s", save_folder)
        os.makedirs(save_folder)

    _download_EMNIST_dataset()


def _download_EMNIST_dataset():
    if os.path.isfile(_CACHE_FILE_PATH):
        os.remove(_CACHE_FILE_PATH)

    _logger.info(f"Downloading {_SOURCE_URL} to {_CACHE_FILE_PATH}.")
    temp_path = _CACHE_FILE_PATH + "_partial"

    try:
        _download_dataset_to_temporary_file(temp_path)
    except Exception:
        _logger.error("Download failed, cleaning temporary directories...")
        os.remove(temp_path)
        raise

    os.rename(temp_path, _CACHE_FILE_PATH)
    _logger.info("Successfully downloaded %s to %s.",
                 _SOURCE_URL, _CACHE_FILE_PATH)


def _download_dataset_to_temporary_file(temp_file_path: str) -> None:
    with open(temp_file_path, 'wb') as temp_file:
        with requests.get(_SOURCE_URL, stream=True, headers=_HEADERS) as response:
            response.raise_for_status()
            chunk_size = 2**13  # 8Kb
            for chunk in response.iter_content(chunk_size=chunk_size):
                temp_file.write(chunk)


def _parse_idx_file_into_numpy_array(data: bytes) -> np.ndarray:
    if data[0] != 0 or data[1] != 0:
        raise ValueError("Data is not in IDX format.")

    shape = _decode_data_shape_bytes(data)
    data_type = _decode_data_type_bytes(data)
    offset = 4 * (data[3] + 1)
    dtype = np.dtype(data_type).newbyteorder('>')
    parsed_data = np.frombuffer(data[offset:], dtype=dtype)
    return parsed_data.reshape(shape)


def _decode_data_shape_bytes(data: bytes):
    dimensions = data[3]
    dimension_byte_length = 4

    if not dimensions:
        raise ValueError("Header indicates zero-dimensional data.")

    shape: list[int] = []
    for dim in range(dimensions):
        offset = dimension_byte_length * (dim + 1)
        dimension_bytes = data[offset:offset + 4]
        dim_size = int(np.frombuffer(dimension_bytes, dtype='>u4')[0])
        shape.append(dim_size)

    return shape


def _decode_data_type_bytes(data: bytes) -> type:
    IDX_DATA_TYPES: dict[int, type] = {
        0x08: np.ubyte,
        0x09: np.byte,
        0x0B: np.int16,
        0x0C: np.int32,
        0x0D: np.float32,
        0x0E: np.float64,
    }

    data_type_bytes = data[2]
    data_type = IDX_DATA_TYPES.get(data_type_bytes)

    if data_type is None:
        raise ValueError(f"Unrecognized data type {hex(data_type_bytes)}.")

    return data_type
