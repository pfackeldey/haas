from __future__ import annotations

import logging
from concurrent import futures

import grpc
import hist
import numpy as np

from haas.protos import hist_pb2, hist_pb2_grpc
from haas.serialize import deserialize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("haas-server")


class Histogrammer(hist_pb2_grpc.HistogrammerServiceServicer):
    def __init__(self, hist: hist.Hist) -> None:
        super().__init__()
        self.hist = hist

    async def Fill(
        self, request: hist_pb2.FillRequest, context: grpc.ServicerContext
    ) -> hist_pb2.FillResponse:
        del context  # unused

        try:
            # Deserialize the message from the request
            kwargs = {key: deserialize(msg) for key, msg in request.kwargs.items()}
        except Exception as e:
            return hist_pb2.FillResponse(
                success=False, message=f"Error deserializing request: {e!r}"
            )
        try:
            self.hist.fill(**kwargs)
            nbytes_filled = sum(
                [nd.nbytes for nd in kwargs.values() if isinstance(nd, np.ndarray)]
            )
            logger.info(f"Filled histogram with {nbytes_filled:,} bytes")
            return hist_pb2.FillResponse(
                success=True,
                message=f"Histogram filled {kwargs!r} successfully! Now is: {self.hist!r}",
            )
        except Exception as e:
            return hist_pb2.FillResponse(
                success=False, message=f"Error filling histogram: {e!r}"
            )

    async def Flush(
        self, request: hist_pb2.FlushRequest, context: grpc.ServicerContext
    ) -> hist_pb2.FlushResponse:
        import h5py
        import uhi.io.hdf5

        del context  # unused

        destination = request.destination
        if not destination.endswith(("h5", ".hdf5")):
            return hist_pb2.FlushResponse(
                success=False,
                message=f"Invalid destination: {destination}, needs to be a hdf5 file, e.g., 'hist.hdf5'.",
            )

        try:
            with h5py.File(destination, "w") as h5_file:
                uhi.io.hdf5.write(h5_file.create_group("histogram"), self.hist)

            logger.info(f"Flushed histogram to {destination}")
            return hist_pb2.FlushResponse(
                success=True,
                message=f"Histogram flushed successfully to {destination}.",
            )
        except Exception as e:
            return hist_pb2.FlushResponse(
                success=False,
                message=f"Error flushing histogram: {e!r} to {destination}",
            )


class Server:
    def __init__(
        self, histogram: hist.Hist, port: int = 50051, n_threads: int = 1
    ) -> None:
        self.port = port
        self.n_threads = n_threads

        # create gRPC server
        self.server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=n_threads),
            # compression=grpc.Compression.Gzip,
            compression=grpc.Compression.NoCompression,  # turn off for now, we compress with numcodecs the byte buffer
            options=[
                ("grpc.max_receive_message_length", 1 << 29),
            ],
        )
        # add service
        histogrammer = Histogrammer(hist=histogram)
        hist_pb2_grpc.add_HistogrammerServiceServicer_to_server(
            histogrammer, self.server
        )

        # add port
        self.server.add_insecure_port(self.address)

    @property
    def address(self) -> str:
        return f"[::]:{self.port}"

    async def start(self) -> None:
        await self.server.start()
        logger.info(
            f"Histogram server started, listening on {self.address} with {self.n_threads} threads"
        )

    async def stop(self, grace: float | None = None) -> None:
        await self.server.stop(grace=grace)

    async def wait_for_termination(self, timeout: float | None = None) -> None:
        await self.server.wait_for_termination(timeout=timeout)
