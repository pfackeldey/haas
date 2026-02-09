from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class FillRequest(_message.Message):
    __slots__ = ("kwargs",)
    class KwargsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Value
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[Value, _Mapping]] = ...,
        ) -> None: ...

    KWARGS_FIELD_NUMBER: _ClassVar[int]
    kwargs: _containers.MessageMap[str, Value]
    def __init__(self, kwargs: _Optional[_Mapping[str, Value]] = ...) -> None: ...

class FlushRequest(_message.Message):
    __slots__ = ("destination",)
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    destination: str
    def __init__(self, destination: _Optional[str] = ...) -> None: ...

class FillResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class FlushResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class Dtype(_message.Message):
    __slots__ = ("type",)
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DT_FLOAT32: _ClassVar[Dtype.Type]
        DT_FLOAT64: _ClassVar[Dtype.Type]
        DT_INT32: _ClassVar[Dtype.Type]
        DT_INT64: _ClassVar[Dtype.Type]

    DT_FLOAT32: Dtype.Type
    DT_FLOAT64: Dtype.Type
    DT_INT32: Dtype.Type
    DT_INT64: Dtype.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: Dtype.Type
    def __init__(self, type: _Optional[_Union[Dtype.Type, str]] = ...) -> None: ...

class Ndarray(_message.Message):
    __slots__ = ("shape", "dtype", "data")
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    shape: _containers.RepeatedScalarFieldContainer[int]
    dtype: Dtype
    data: bytes
    def __init__(
        self,
        shape: _Optional[_Iterable[int]] = ...,
        dtype: _Optional[_Union[Dtype, _Mapping]] = ...,
        data: _Optional[bytes] = ...,
    ) -> None: ...

class Value(_message.Message):
    __slots__ = ("array_value", "string_value", "int_value", "bool_value")
    ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    array_value: Ndarray
    string_value: str
    int_value: int
    bool_value: bool
    def __init__(
        self,
        array_value: _Optional[_Union[Ndarray, _Mapping]] = ...,
        string_value: _Optional[str] = ...,
        int_value: _Optional[int] = ...,
        bool_value: bool = ...,
    ) -> None: ...
