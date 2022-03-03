#!/usr/bin/env bash

# Write the generated public key ca certificate to disk,
# for usage from the command-line.
docker-compose cp elasticsearch1:/usr/share/elasticsearch/config/certs/ca/ca.crt .
