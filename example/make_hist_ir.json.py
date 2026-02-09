from __future__ import annotations

import json

import hist
import uhi.io.json

if __name__ == "__main__":
    # define example histogram that we fill remotely (see example/client.py)
    H = hist.Hist(
        hist.axis.Regular(10, -2, 2, name="x", label="X Axis"),
        hist.axis.Regular(10, -2, 2, name="y", label="Y Axis"),
        # hardcoding the categorical axes because uhi serialization doesn't support growth=True yet
        hist.axis.StrCategory(
            ["data", "drell-yan"], name="dataset", label="Dataset", growth=True
        ),
        storage=hist.storage.Weight(),
    )

    # write IR to file
    with open("example/hist_ir.json", "w") as f:
        json.dump(H, f, indent=2, default=uhi.io.json.default)
