FROM postgres:latest

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i '/pt_BR.UTF-8/s/^# //' /etc/locale.gen && \
    locale-gen

ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:pt
ENV LC_ALL=pt_BR.UTF-8
