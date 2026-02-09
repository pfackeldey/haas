#!/usr/bin/env bash

action() {
    haas-server --port 50051 --n-threads 4 --hist-ir "$(cat example/hist_ir.json)"
}
action "$@"
