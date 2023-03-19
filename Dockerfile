FROM python:3.10-alpine

RUN mkdir /app &&\
    apt install curl
    pip3 install waitress &&\
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" &&\
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl &&\
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 &&\
    chmod 700 get_helm.sh &&\
    ./get_helm.sh &&\

WORKDIR /app

COPY app /app

RUN  

ENTRYPOINT ["waitress-serve", "--port", "80", "app:app"]