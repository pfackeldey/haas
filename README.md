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
#   Regular(10, -2, 2, name='x', label='X Axis'),
#   Regular(10, -2, 2, name='y', label='Y Axis'),
#   StrCategory(['data', 'drell-yan'], overflow=False, name='dataset', label='Dataset'),
#   storage=Weight()) # Sum: WeightedSum(value=0, variance=0)
# INFO:haas-server:Histogram server started, listening on [::]:50051 with max_workers=1
```

Run example client:
```shell
python example/client.py
# Histogram remote_hist received: Histogram filled {'y': array([ 0.88330122, -0.13018699,  0.30395399, ...,  0.05815926,
#         0.0319339 ,  0.6173756 ], shape=(1000000,)), 'x': array([-0.39557326, -1.10047103, -0.25452045, ..., -0.91580713,
#         0.85419406,  0.14931346], shape=(1000000,)), 'weight': array([1., 1., 1., ..., 1., 1., 1.], shape=(1000000,)), 'dataset': # 'data'} successfully! Now is: Hist(
#   Regular(10, -2, 2, name='x', label='X Axis'),
#   Regular(10, -2, 2, name='y', label='Y Axis'),
#   StrCategory(['data', 'drell-yan'], overflow=False, name='dataset', label='Dataset'),
#   storage=Weight()) # Sum: WeightedSum(value=911141, variance=911141) (WeightedSum(value=1e+06, variance=1e+06) with flow)

# Histogram remote_hist received: Histogram filled {'y': array([-0.7015261 , -2.24620403, -1.44075752, ..., -1.01488795,
#         1.04233221,  1.71569615], shape=(1000000,)), 'x': array([ 0.505213  ,  0.90704077, -0.84626962, ..., -0.89036558,
#         1.0678381 , -0.04706042], shape=(1000000,)), 'weight': array([1., 1., 1., ..., 1., 1., 1.], shape=(1000000,)), 'dataset': 'drell-yan'} successfully! Now is: Hist(
#   Regular(10, -2, 2, name='x', label='X Axis'),
#   Regular(10, -2, 2, name='y', label='Y Axis'),
#   StrCategory(['data', 'drell-yan'], overflow=False, name='dataset', label='Dataset'),
#   storage=Weight()) # Sum: WeightedSum(value=1.82276e+06, variance=1.82276e+06) (WeightedSum(value=2e+06, variance=2e+06) with flow)
#
# Histogram remote_hist received: Histogram flushed successfully to hist.coffea.
```

And the server logs additionally (after running the client script):
```shell
# INFO:haas-server:Filled histogram with 24,000,000 bytes
# INFO:haas-server:Filled histogram with 24,000,000 bytes
# INFO:haas-server:Flushed histogram to hist.coffea
```

## Current supported types

Axis support:
- `hist.axis.Regular`
- `hist.axis.Boolean`
- `hist.axis.Variable`
- `hist.axis.Integer`
- `hist.axis.IntCategory`
- `hist.axis.StrCategory`

`np.dtype` support for `hist.axis.{Regular,Variable,Integer}`:
- `np.float64`
- `np.float32`
- `np.int64`
- `np.int32`


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