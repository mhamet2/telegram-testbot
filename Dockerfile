FROM centos:centos7
MAINTAINER Jordi Prats
ENV HOME /root

RUN yum install epel-release -y
RUN yum install git -y
RUN yum install curl -y
RUN yum install python-setuptools.noarch -y

RUN mkdir -p /usr/local/src/python-telegram-bot
RUN mkdir -p /usr/local/src/perbot

RUN git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive /usr/local/src/python-telegram-bot

RUN bash -c 'cd /usr/local/src/python-telegram-bot; python setup.py install'

RUN mkdir -p /opt/telegram/perbot

COPY perbot.py /opt/telegram/perbot/perbot.py
COPY perbot.config /opt/telegram/perbot/perbot.config
