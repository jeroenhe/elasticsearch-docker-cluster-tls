# Elasticsearch cluster in docker

This project provides you with an elasticsearch cluster consisting of three elasticsearch instances, using the basic license. I've created it during and after the Elastic Engineer training to help me with a ready-to-go environment where I can play with the training labs. It is based on my [https://github.com/jeroenhendricksen/elasticsearch-docker-cluster] with the difference that this project has TLS and RBAC enabled. This example was insired by (or rather copied from) [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-compose-file).

Disclaimer: this setup is not meant for production usage!

## Prerequisites

- a machine with enough RAM (at least 8 gb)
- `docker` and `docker-compose` installed (on Mac or Windows, Docker Desktop installs both of them).

## Elasticsearch indices

Some example indices are created at startup:

### `test-index`

Docker container `es-writer` writes data continuously to index `test-index` and reads it using container `es-reader`, all using python scripts and the [official low-level elasticsearch python client library](https://pypi.org/project/elasticsearch/). [View the data](http://localhost:9200/test-index/_search?pretty=true&size=10).

### `blogs`

Example taken from the [Elastic Engineer I training](https://training.elastic.co/instructor-led-training/ElasticsearchEngineerI) containing an excerpt from their online blogs. The index is created (once) from a [csv](logstash-ingest/data/blogs.csv) file using the `logstash-ingest` docker container.
[View the data](http://localhost:9200/blogs/_search?pretty=true&size=1). This is a Static Dataset.

### `logs_server*`

Example taken from the [Elastic Engineer I training](https://training.elastic.co/instructor-led-training/ElasticsearchEngineerI) as well, containing an excerpt from websserver access logs for the [elastic blogs website](https://www.elastic.co/blog/). [View the data](http://localhost:9200/logs_server*/_search?pretty=true&size=1). This is a Time Series Dataset. It can take a while to import this entirely.

## Get it up and running

Make sure you provide docker with enough memory (the default 2gb of memory is not enough, consult your Docker Desktop configuration to change this), before you run it with

    docker-compose up -d

OR

    ./run.sh

Confirm that elasticsearch is healthy (it can take quite some time) by visiting one of the following links from your browser or a tool like curl or [httpie](https://httpie.org/):

Elastic search nodes:

Note: you should ignore the ssl warning when visiting the url's below (or trust ca/ca.crt as CA from your browser and add elasticsearch{1,3} to your local hosts file)
Note 2: basic authentication is enabled. You should provide the `elastic` user and its password which is set in `.env`.

- [cluster health](https://localhost:9200/_cluster/health?pretty=true)
- [cluster nodes](https://localhost:9200/_nodes/_all/http?pretty=true)
- [elasticsearch1 node health](https://localhost:9200/_cat/health)
- [elasticsearch2 node health](https://localhost:9201/_cat/health)
- [elasticsearch3 node health](https://localhost:9202/_cat/health)

Other services:

- [Kibana](http://localhost:5601). Login to kibana via APP_USER and APP_PASSWORD stored in `.env`.
- [All five indices in Kibana](http://localhost:5601/app/kibana#/management/elasticsearch/index_management/indices?_g=())

## Snapshots

A folder has been bind-mounted to all elasticsearch nodes already with the purpose of sharing snapshots with the docker host. This folder is relative from this directory: `./shared_folder`.
When registering a (fs-type) snapshot repository inside elasticsearch, you should make it point to `/shared_folder` from inside the container.

## RBAC related commands

    # Add a new user:
    docker-compose exec elasticsearch1 /bin/bash
    bin/elasticsearch-users useradd newelastic -p newelastic1 -r superuser

    # Resets an existing user' password:
    docker-compose exec elasticsearch1 /bin/bash
    elasticsearch-reset-password -b -u elastic --url https://elasticsearch1:9200
    Password for the [elastic] user successfully reset.
    New value: xxxxx

    # Change a user password (works for non-system accounts):
    docker-compose exec elasticsearch1 /bin/bash
    bin/elasticsearch-users passwd UserToChangePasswordFor

## Test a service

    docker-compose run --no-deps logstash-ingest /bin/bash
    docker-compose run --no-deps filebeat-ingest /bin/bash

## Investigate certs

Certificates are created at the setup' container startup. To investigate

    docker run -it --rm -v estls_certs:/ssl ubuntu:20.04 /bin/bash
    cd /ssl
    ls -la

## Cleanup

Clean all created containers and volumes by executing:

    docker-compose down -v

or

    ./cleanup.sh

If you experience problems, this can also help to solve them by 'starting over'.

## ToDo

- Add cloud-enabled snapshot backups (to Azure or Amazon) including documentation
