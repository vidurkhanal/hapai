#!/bin/bash

docker build -t vidurkhanal/minisrv-notifications:latest .
docker push vidurkhanal/minisrv-notifications:latest
kubectl delete -f manifests/
kubectl apply -f manifests/