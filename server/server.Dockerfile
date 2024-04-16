FROM python:3.10.9-bullseye

ENV SERVER_HOME /home/app/server
RUN mkdir -p $SERVER_HOME
WORKDIR $SERVER_HOME

ENV PORT 8080

COPY . $SERVER_HOME

EXPOSE $PORT

RUN pip install -r requirements.txt
