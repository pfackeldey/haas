from __future__ import annotations

import typing as tp
import numpy as np

from haas.protos import hist_pb2


def serialize(item: tp.Any) -> hist_pb2.Value:
    """Serialize something into a hist_pb2.Value message."""
    msg = hist_pb2.Value()
    if isinstance(item, np.ndarray):
        shape = list(item.shape)
        dtype = _numpy_dtype_to_proto_dtype(item.dtype)
        data = item.tobytes()
        msg.array_value.CopyFrom(hist_pb2.ndarray(shape=shape, dtype=dtype, data=data))
    elif isinstance(item, str):
        msg.string_value = item
    elif isinstance(item, int):
        msg.int_value = item
    elif isinstance(item, bool):
        msg.bool_value = item
    else:
        raise TypeError(f"Can't serialize: {item}")
    return msg


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


def deserialize(message: hist_pb2.Value):
    """Deserialize a hist_pb2.Value message into a numpy ndarray, str or int."""
    match message.WhichOneof("value"):
        case "array_value":
            ndarray = message.array_value
            shape = tuple(ndarray.shape)
            dtype = _proto_dtype_to_numpy_dtype(ndarray.dtype)
            array = np.frombuffer(ndarray.data, dtype=dtype).reshape(shape)
            return array
        case "string_value":
            return message.string_value
        case "int_value":
            return message.int_value
        case "bool_value":
            return message.bool_value
        case _:
            raise ValueError("Unsupported Value type")


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
