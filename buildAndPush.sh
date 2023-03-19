#!/bin/bash

docker build . -t docker.io/jozseftorocsik/szakdolgozat-deployer --no-cache
docker push docker.io/jozseftorocsik/szakdolgozat-deployer


helm uninstall deployer -n apps
helm install deployer ./helm/deployer -n apps