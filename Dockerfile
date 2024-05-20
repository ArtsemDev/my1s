FROM python:3.11.7-alpine3.19

WORKDIR /opt
COPY . /opt
RUN pip install -r /opt/requirements.txt
