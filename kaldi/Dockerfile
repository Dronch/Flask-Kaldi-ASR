FROM ubuntu

RUN apt-get update --fix-missing \
    && apt-get install -y python3.6 python3-pip libsndfile1

RUN mkdir /opt/api-sr
COPY ./web/api-sr/requirements.txt /opt/api-sr
WORKDIR /opt/api-sr
RUN pip3 install -r requirements.txt

COPY ./web/api-sr /opt/api-sr

RUN chmod +x init_workers.sh
CMD ./init_workers.sh

