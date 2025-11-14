#!/usr/bin/env bash

action() {
    haas-server --port 50051 --max-workers 1 --hist-ir "$(cat example/hist_ir.json)"
}
action "$@"
