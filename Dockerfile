FROM ubuntu:20.04

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install nano
RUN apt-get install cron -y

RUN mkdir /home/schmuck
WORKDIR home/schmuck

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY crontab ./

CMD crontab crontab

CMD cron -f
