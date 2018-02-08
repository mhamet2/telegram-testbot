FROM centos:centos7
MAINTAINER Jordi Prats
ENV HOME /root

RUN yum install epel-release -y
RUN yum install git -y
RUN yum install curl -y
RUN yum install python-setuptools.noarch -y
RUN yum install python-pip -y

RUN pip install tabulate

RUN mkdir -p /usr/local/src/testbot

RUN mkdir -p /usr/local/src/python-telegram-bot
RUN git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive /usr/local/src/python-telegram-bot
RUN bash -c 'cd /usr/local/src/python-telegram-bot; python setup.py install'

RUN mkdir -p /usr/local/src/emoji
RUN git clone https://github.com/carpedm20/emoji.git /usr/local/src/emoji
RUN bash -c 'cd /usr/local/src/emoji; python setup.py install'

RUN mkdir -p /opt/telegram/testbot

COPY testbot.py /opt/telegram/testbot/testbot.py
COPY testbot.config /opt/telegram/testbot/testbot.config
