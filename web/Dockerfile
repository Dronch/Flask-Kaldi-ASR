FROM ubuntu

RUN apt-get update --fix-missing \
    && apt-get install -y python3.6 python3-pip libsndfile1

RUN mkdir /opt/api-sr
COPY api-sr/requirements.txt /opt/api-sr
WORKDIR /opt/api-sr
RUN pip3 install -r requirements.txt && pip3 install gunicorn

COPY api-sr /opt/api-sr

RUN chmod +x run.sh
CMD ./run.sh

