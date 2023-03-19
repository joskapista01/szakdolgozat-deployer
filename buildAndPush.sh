#!/bin/bash

docker build . -t docker.io/jozseftorocsik/szakdolgozat-deployer --no-cache
docker push docker.io/jozseftorocsik/szakdolgozat-deployer


#helm uninstall api -n apps
#helm install api ./helm/api -n apps