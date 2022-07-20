#!/bin/bash

docker build -t vidurkhanal/minisrv-gateway:latest .
docker push vidurkhanal/minisrv-gateway:latest
kubectl delete -f manifests/
kubectl apply -f manifests/