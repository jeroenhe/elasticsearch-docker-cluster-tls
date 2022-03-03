FROM docker.elastic.co/beats/filebeat:8.0.0

USER root

COPY *.sh /
RUN chmod 755 /*.sh

RUN mkdir /var/log/filebeat
RUN chown filebeat /var/log/filebeat -R

USER filebeat

CMD [ "/run.sh" ]
