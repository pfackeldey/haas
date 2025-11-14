# Histogramming as a Service (HaaS)

## Install
```shell
uv pip install .
```

## Example

See `example/`.

Start gRPC server (or just `./example/start_server.sh`):
```shell
haas-server --port 50051 --max-workers 1 --hist-ir "$(cat example/hist_ir.json)"
# INFO:haas-server:Histogram setup successfully: Hist(
#   Regular(50, -5, 5, name='x', label='X Axis'),
#   Regular(50, -5, 5, name='y', label='Y Axis'),
#   storage=Double())
# INFO:haas-server:Histogram server started, listening on [::]:50051 with max_workers=1
```

Run example client:
```shell
python example/client.py
# Histogram remote_hist received: Histogram filled {'y': array([-0.4310625 , -0.54584864, -1.6486728 , ...,  1.42684052,
#        -1.38751229,  0.42781165], shape=(1000000,)), 'x': array([ 0.88761779,  0.1662822 ,  0.83310628, ..., -2.05403307,
#         1.79718163, -1.08342469], shape=(1000000,))} successfully! Now is: Hist(
#   Regular(50, -5, 5, name='x', label='X Axis'),
#   Regular(50, -5, 5, name='y', label='Y Axis'),
#   storage=Double()) # Sum: 1000000.0
#
# Histogram remote_hist received: Histogram flushed successfully to hist.coffea.
```

And the server logs additionally (after running the client script):
```shell
# INFO:haas-server:Filled histogram with 16,000,000 bytes
# INFO:haas-server:Flushed histogram to hist.coffea
```

## Developer Info

### Install
```shell
uv pip install -e . --group=dev
```

### protobuf codegen

```shell
python -m grpc_tools.protoc -Isrc/haas/protos --python_out=src/haas/protos --pyi_out=src/haas/protos --grpc_python_out=src/haas/protos src/haas/protos/hist.proto
```
Maybe adjust imports in `src/haas/protos/hist_pb2_grpc.py`.