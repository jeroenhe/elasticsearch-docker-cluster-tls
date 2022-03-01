#!/usr/bin/env bash

/wait-for-it.sh -h elasticsearch1 -p 9200 -t 180

echo "Verify index does not yet exist, so we import it only once..."

if [ ! -f "${ES_SSL_CA}" ]; then
    echo "ES_SSL_CA ($ES_SSL_CA) does not exists!"
    exit 1
fi

curl -sSf --cacert "${ES_SSL_CA}" "https://elasticsearch1:9200/blogs/_count" -u "${ES_AUTH_USERNAME}:${ES_AUTH_PASSWORD}" 1>/dev/null
EXIT_CODE=$?

echo "Curl exited with '${EXIT_CODE}'"

if [ "${EXIT_CODE}" != "0" ]; then
    echo "Starting CSV import for /data/blogs.csv..."
    ./bin/logstash -f /data/blogs_csv.conf
else
    echo "Index blog was already imported. Skipping."
fi

exit 0
