from __future__ import annotations

from concurrent import futures

import logging
import cloudpickle
import fsspec
import hist
import grpc
from haas.protos import hist_pb2_grpc, hist_pb2

from haas.serialize import deserialize_ndarray

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("haas-server")


class Histogrammer(hist_pb2_grpc.HistogrammerServicer):
    def __init__(self, hist: hist.Hist) -> None:
        super().__init__()
        self.hist = hist

    def fill(
        self, request: hist_pb2.FillRequest, context: grpc.ServicerContext
    ) -> hist_pb2.Result:
        del context  # unused

        try:
            # Deserialize the ndarrays from the request
            kwargs = {
                key: deserialize_ndarray(array_msg)
                for key, array_msg in request.kwargs.items()
            }
        except Exception as e:
            return hist_pb2.Result(
                success=False, message=f"Error deserializing request: {e!r}"
            )
        try:
            self.hist.fill(**kwargs)
            logger.info(f"Filled histogram with {sum([nd.nbytes for nd in kwargs.values()]):,} bytes")
            return hist_pb2.Result(
                success=True,
                message=f"Histogram filled {kwargs!r} successfully! Now is: {self.hist!r}",
            )
        except Exception as e:
            return hist_pb2.Result(
                success=False, message=f"Error filling histogram: {e!r}"
            )

    def flush(
        self, request: hist_pb2.FlushRequest, context: grpc.ServicerContext
    ) -> hist_pb2.Result:
        del context  # unused

        destination = request.destination

        try:
            with fsspec.open(destination, "wb", compression="lz4") as fout:
                cloudpickle.dump(self.hist, fout)

            logger.info(f"Flushed histogram to {destination}")
            return hist_pb2.Result(
                success=True,
                message=f"Histogram flushed successfully to {destination}.",
            )
        except Exception as e:
            return hist_pb2.Result(
                success=False,
                message=f"Error flushing histogram: {e!r} to {destination}",
            )


class Server:
    def __init__(self, histogram: hist.Hist, port: int = 50051, max_workers: int = 1) -> None:
        self.port = port
        self.max_workers = max_workers

        # create gRPC server
        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            compression=grpc.Compression.Gzip,
            options=[
                ("grpc.max_receive_message_length", 1 << 29),
            ],
        )
        # add service
        histogrammer = Histogrammer(hist=histogram)
        hist_pb2_grpc.add_HistogrammerServicer_to_server(histogrammer, self.server)

        # add port
        self.server.add_insecure_port(self.address)

    @property
    def address(self) -> str:
        return f"[::]:{self.port}"

    def start(self) -> None:
        self.server.start()
        logger.info(f"Histogram server started, listening on {self.address} with max_workers={self.max_workers}")

    def stop(self, grace: float | None = None) -> None:
        self.server.stop(grace=grace)

    def wait_for_termination(self, timeout: float | None = None) -> None:
        self.server.wait_for_termination(timeout=timeout)
