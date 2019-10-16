FROM python:3.7.4

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip3 install -r requirements.txt
