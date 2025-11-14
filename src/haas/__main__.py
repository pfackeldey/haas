from __future__ import annotations

import logging
import hist
import uhi.io.json
import json
from argparse import ArgumentParser
from haas.server import Server, logger


def main():
    ap = ArgumentParser()
    ap.add_argument("-p", "--port", default=0, type=int)
    ap.add_argument("-w", "--max-workers", default=1, type=int)
    ap.add_argument(
        "--hist-ir", default=None, type=str, help="JSON Hist IR", required=True
    )

    args = ap.parse_args()

    assert 0 <= args.port < 0xFFFF, "port must be between 0 and 65535"

    # load histogram from JSON IR
    hist_ir = json.loads(args.hist_ir, object_hook=uhi.io.json.object_hook)
    histogram = hist.Hist(hist_ir)

    logger.info(f"Histogram setup successfully: {histogram}")

    # start server
    server = Server(histogram=histogram, port=args.port, max_workers=args.max_workers)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
