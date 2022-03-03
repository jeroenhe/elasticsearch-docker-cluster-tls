#!/usr/bin/env bash

/wait-for-it.sh -h elasticsearch1 -p 9200 -t 180

echo "Verify index does not yet exist, so we import it only once..."

if [ ! -f "${ES_SSL_CA}" ]; then
    echo "ES_SSL_CA ($ES_SSL_CA) does not exists!"
    exit 1
fi

curl -sSf --cacert "${ES_SSL_CA}" "https://elasticsearch1:9200/logs_server1/_count" -u "${ES_AUTH_USERNAME}:${ES_AUTH_PASSWORD}" 1>/dev/null
EXIT_CODE=$?

echo "Curl exited with '${EXIT_CODE}'"

if [ "${EXIT_CODE}" != "0" ]; then
    echo "Starting log files import for /data/elastic*..."
    # Debug: ./filebeat -e -d "*" -c /data/filebeat.yml
    ./filebeat -c /data/filebeat.yml
else
    echo "Indices logs_server* were already imported. Skipping."
fi

exit 0
