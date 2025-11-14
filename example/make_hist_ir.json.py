from __future__ import annotations

import hist
import json
import uhi.io.json


if __name__ == "__main__":
    # define example histogram that we fill remotely (see example/client.py)
    H = hist.Hist(
        hist.axis.Regular(50, -5, 5, name="x", label="X Axis"),
        hist.axis.Regular(50, -5, 5, name="y", label="Y Axis"),
        storage=hist.storage.Double(),
    )

    # write IR to file
    with open("example/hist_ir.json", "w") as f:
        json.dump(H, f, indent=2, default=uhi.io.json.default)