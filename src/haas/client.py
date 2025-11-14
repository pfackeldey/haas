from __future__ import annotations

import numpy as np
import grpc
from functools import cached_property
from haas.protos import hist_pb2_grpc, hist_pb2

from haas.serialize import serialize_ndarray

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HaaSClient:
    def __init__(self, address: str) -> None:
        self.address = address

    def __getstate__(self):
        state = dict(self.__dict__)
        state.pop("channel", None)
        return state
    
    def __enter__(self) -> HaaSClient:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        del exc_type, exc_value, traceback  # unused
        self.channel.close()

    @cached_property
    def channel(self) -> grpc.Channel:
        return grpc.insecure_channel(
            self.address,
            compression=grpc.Compression.Gzip,
            options=[
                ("grpc.max_send_message_length", 1 << 29),
                ("grpc.max_receive_message_length", 1 << 29),
            ],
        )

    @property
    def stub(self) -> hist_pb2_grpc.HistogrammerStub:
        return hist_pb2_grpc.HistogrammerStub(self.channel)

    def fill(self, **kwargs: np.ndarray) -> hist_pb2.Result:
        serialized_kwargs = {
            key: serialize_ndarray(array) for key, array in kwargs.items()
        }
        request = hist_pb2.FillRequest(kwargs=serialized_kwargs)
        return self.stub.fill(request)

    def flush(self, destination: str = "hist.coffea") -> hist_pb2.Result:
        request = hist_pb2.FlushRequest(destination=destination)
        return self.stub.flush(request)
