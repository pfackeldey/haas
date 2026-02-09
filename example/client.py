from __future__ import annotations

import numpy as np

from haas import HaaSClient

if __name__ == "__main__":
    # connect to remote HaaS gRPC server
    with HaaSClient(address="[::]:50051") as remote_hist:
        # fill histogram remotely, returns futures
        response_future = remote_hist.fill(
            x=np.random.normal(size=1_000_000).astype(np.float64),
            y=np.random.normal(size=1_000_000).astype(np.float64),
            dataset="data",
            weight=np.ones(1_000_000, dtype=np.float64),
        )
        print(f"Histogram remote_hist received: {response_future.result().message}\n")

        # fill histogram remotely again with different dataset
        response_future = remote_hist.fill(
            x=np.random.normal(size=1_000_000).astype(np.float64),
            y=np.random.normal(size=1_000_000).astype(np.float64),
            dataset="drell-yan",
            weight=np.ones(1_000_000, dtype=np.float64),
        )
        print(f"Histogram remote_hist received: {response_future.result().message}\n")

        # fill histogram remotely again with different dataset (something that triggers axis growth)
        response_future = remote_hist.fill(
            x=np.random.normal(size=1_000_000).astype(np.float64),
            y=np.random.normal(size=1_000_000).astype(np.float64),
            dataset="ttbar",
            weight=np.ones(1_000_000, dtype=np.float64),
        )
        print(f"Histogram remote_hist received: {response_future.result().message}\n")

        # flush histogram remotely to file
        response_future = remote_hist.flush(destination="hist.h5")
        print(f"Histogram remote_hist received: {response_future.result().message}\n")
