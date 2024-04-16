FROM python:3.10.9-bullseye

ENV CRON_HOME /home/app/cron
RUN mkdir -p $CRON_HOME
WORKDIR $CRON_HOME

COPY . $CRON_HOME

RUN ln -sf /usr/bin/python3 /usr/bin/python

RUN pip install -r requirements.txt

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y cron

RUN mkdir -p ./area/log
RUN touch ./area/log/debug.log

RUN ./area/manage.py crontab add
