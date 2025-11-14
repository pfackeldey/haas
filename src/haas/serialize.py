from __future__ import annotations

import numpy as np

from haas.protos import hist_pb2


def serialize_ndarray(array) -> hist_pb2.ndarray:
    """Serialize a numpy ndarray into a hist_pb2.ndarray message."""

    if not isinstance(array, np.ndarray):
        raise TypeError("Input must be a numpy ndarray.")

    shape = list(array.shape)
    dtype = _numpy_dtype_to_proto_dtype(array.dtype)

    data = array.tobytes()

    return hist_pb2.ndarray(shape=shape, dtype=dtype, data=data)


def _numpy_dtype_to_proto_dtype(np_dtype: np.dtype) -> hist_pb2.dtype:
    """Mapping from numpy dtypes to hist_pb2.dtype messages."""
    match np_dtype:
        case np.float32:
            return hist_pb2.dtype(type=hist_pb2.dtype.DT_FLOAT32)
        case np.float64:
            return hist_pb2.dtype(type=hist_pb2.dtype.DT_FLOAT64)
        case np.int32:
            return hist_pb2.dtype(type=hist_pb2.dtype.DT_INT32)
        case np.int64:
            return hist_pb2.dtype(type=hist_pb2.dtype.DT_INT64)
        case _:
            raise ValueError(f"Unsupported numpy dtype: {np_dtype}")


def deserialize_ndarray(message: hist_pb2.ndarray):
    """Deserialize a hist_pb2.ndarray message into a numpy ndarray."""

    if not isinstance(message, hist_pb2.ndarray):
        raise TypeError("Input must be a hist_pb2.ndarray message.")

    shape = tuple(message.shape)
    dtype = _proto_dtype_to_numpy_dtype(message.dtype)

    array = np.frombuffer(message.data, dtype=dtype).reshape(shape)

    return array


def _proto_dtype_to_numpy_dtype(proto_dtype: hist_pb2.dtype) -> np.dtype:
    """Mapping from hist_pb2.dtype messages to numpy dtypes."""
    match proto_dtype.type:
        case hist_pb2.dtype.DT_FLOAT32:
            return np.float32
        case hist_pb2.dtype.DT_FLOAT64:
            return np.float64
        case hist_pb2.dtype.DT_INT32:
            return np.int32
        case hist_pb2.dtype.DT_INT64:
            return np.int64
        case _:
            raise ValueError(f"Unsupported proto dtype: {proto_dtype.type}")
