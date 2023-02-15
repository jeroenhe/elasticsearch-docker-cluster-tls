ARG STACK_VERSION
FROM docker.elastic.co/beats/filebeat:${STACK_VERSION}

USER root

COPY *.sh /
RUN chmod 755 /*.sh

RUN mkdir /var/log/filebeat
RUN chown filebeat /var/log/filebeat -R

USER filebeat

CMD [ "/run.sh" ]
