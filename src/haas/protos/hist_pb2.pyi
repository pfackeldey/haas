from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FillRequest(_message.Message):
    __slots__ = ("kwargs",)
    class KwargsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ndarray
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ndarray, _Mapping]] = ...) -> None: ...
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    kwargs: _containers.MessageMap[str, ndarray]
    def __init__(self, kwargs: _Optional[_Mapping[str, ndarray]] = ...) -> None: ...

class FlushRequest(_message.Message):
    __slots__ = ("destination",)
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    destination: str
    def __init__(self, destination: _Optional[str] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class dtype(_message.Message):
    __slots__ = ("type",)
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DT_FLOAT32: _ClassVar[dtype.Type]
        DT_FLOAT64: _ClassVar[dtype.Type]
        DT_INT32: _ClassVar[dtype.Type]
        DT_INT64: _ClassVar[dtype.Type]
    DT_FLOAT32: dtype.Type
    DT_FLOAT64: dtype.Type
    DT_INT32: dtype.Type
    DT_INT64: dtype.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: dtype.Type
    def __init__(self, type: _Optional[_Union[dtype.Type, str]] = ...) -> None: ...

class ndarray(_message.Message):
    __slots__ = ("shape", "dtype", "data")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    shape: _containers.RepeatedScalarFieldContainer[int]
    dtype: dtype
    data: bytes
    def __init__(self, shape: _Optional[_Iterable[int]] = ..., dtype: _Optional[_Union[dtype, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...
