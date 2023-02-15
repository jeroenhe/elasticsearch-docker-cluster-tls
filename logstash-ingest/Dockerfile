ARG STACK_VERSION
FROM docker.elastic.co/logstash/logstash:${STACK_VERSION}

USER root

COPY *.sh /
RUN chmod 755 /*.sh

RUN rm /usr/share/logstash/config/logstash-sample.conf
USER logstash
COPY logstash.yml /usr/share/logstash/config/logstash.yml

CMD [ "/run.sh" ]
