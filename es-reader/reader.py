#!/usr/bin/env python3
import logging
import os
import sys
import time
from datetime import datetime
from elasticsearch import Elasticsearch


LOGGER_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)
LOGGER = logging.getLogger('es-reader')

ES_HOST_SEED = os.environ['ES_HOST_SEED'].split(',')
ES_SSL_CA = None
ES_AUTH_USERNAME = None
ES_AUTH_PASSWORD = None
if 'ES_SSL_CA' in os.environ:
    ES_SSL_CA = os.environ['ES_SSL_CA']
if 'ES_AUTH_USERNAME' in os.environ:
    ES_AUTH_USERNAME = os.environ['ES_AUTH_USERNAME']
if 'ES_AUTH_PASSWORD' in os.environ:
    ES_AUTH_PASSWORD = os.environ['ES_AUTH_PASSWORD']


def read_data():
    # https://elasticsearch-py.readthedocs.io/en/master/
    ssl_options = dict()
    if ES_SSL_CA:
        ssl_options['verify_certs'] = True
        ssl_options['ca_certs'] = ES_SSL_CA
        if ES_AUTH_USERNAME and ES_AUTH_PASSWORD:
            ssl_options['basic_auth'] = (ES_AUTH_USERNAME, ES_AUTH_PASSWORD)
    LOGGER.info("ssl_options: %s", ssl_options)
    es = Elasticsearch(ES_HOST_SEED, sniff_on_start=False, sniff_on_node_failure=True, **ssl_options)
    while True:
        # Count the number of records in our index
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-count.html
        res_count = es.count(index="test-index")
        LOGGER.info("# of records: %s", res_count['count'])
        
        # Search for the latest record
        # https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.search
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html
        res = es.search(index="test-index", size=1, sort={"timestamp": "desc"}, query={"match_all": {}})
        LOGGER.info("Took: %sms, Got %d hits. First hit: %s", res['took'], res['hits']['total']['value'], res['hits']['hits'][0]["_source"])
        time.sleep(5)


def main():
    LOGGER.info("es-reader was started")
    while True:
        try:
            read_data()
        except (KeyboardInterrupt, SystemExit):
            LOGGER.info("Exiting by user request.")
            sys.exit(0)
        except Exception:  # catch *all* exceptions
            LOGGER.error("Fatal error in main loop", exc_info=True)
            sys.exit(1)
        finally:
            LOGGER.info("es-reader was stopped")


if __name__ == "__main__":
    main()
