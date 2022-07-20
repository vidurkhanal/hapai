#!/bin/bash

docker build -t vidurkhanal/minisrv-consumer:latest .
docker push vidurkhanal/minisrv-consumer:latest
kubectl delete -f manifests/
kubectl apply -f manifests/