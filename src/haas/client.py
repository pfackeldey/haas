from __future__ import annotations

import logging
import typing as tp
from functools import cached_property

import grpc

from haas.protos import hist_pb2, hist_pb2_grpc
from haas.serialize import serialize

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
            # compression=grpc.Compression.Gzip,
            compression=grpc.Compression.NoCompression,  # turn off for now, we compress with numcodecs the byte buffer
            options=[
                ("grpc.max_send_message_length", 1 << 29),
            ],
        )

    @property
    def stub(self) -> hist_pb2_grpc.HistogrammerServiceStub:
        return hist_pb2_grpc.HistogrammerServiceStub(self.channel)

    def fill(self, **kwargs: tp.Any) -> grpc.Future[hist_pb2.FillResponse]:
        serialized_kwargs = {key: serialize(value) for key, value in kwargs.items()}
        request = hist_pb2.FillRequest(kwargs=serialized_kwargs)
        return self.stub.Fill.future(request)

    def flush(
        self, destination: str = "hist.coffea"
    ) -> grpc.Future[hist_pb2.FlushResponse]:
        request = hist_pb2.FlushRequest(destination=destination)
        return self.stub.Flush.future(request)
