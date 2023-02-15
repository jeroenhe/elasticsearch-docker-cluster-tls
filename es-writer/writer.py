#!/usr/bin/env python3
import logging
import os
import random
import sys
import time
from datetime import datetime
from elasticsearch import Elasticsearch


LOGGER_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)
LOGGER = logging.getLogger('es-writer')

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


def write_data():
    # https://elasticsearch-py.readthedocs.io/en/master/
    ssl_options = dict()
    if ES_SSL_CA:
        ssl_options['verify_certs'] = True
        ssl_options['ca_certs'] = ES_SSL_CA
        if ES_AUTH_USERNAME and ES_AUTH_PASSWORD:
            ssl_options['basic_auth'] = (ES_AUTH_USERNAME, ES_AUTH_PASSWORD)
    LOGGER.info("ssl_options: %s", ssl_options)
    es = Elasticsearch(ES_HOST_SEED, sniff_on_start=False, sniff_on_node_failure=True, **ssl_options)
    counter=-1
    
    while True:
        counter = counter + 1
        doc = {
            'text': 'Random number #' + str(random.randint(1,1000)),
            'timestamp': datetime.now(),
        }
        # https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.index
        # http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html

        # when this service restarted, the counter is reset. When a document with the same id already
        # exists, it is updated.
        res = es.index(index="test-index", id=counter, document=doc)

        LOGGER.info("Index result for text '%s': %s", doc['text'], res['result'])
        time.sleep(5)


def main():
    LOGGER.info("es-writer was started")
    while True:
        try:
            write_data()
        except (KeyboardInterrupt, SystemExit):
            LOGGER.info("Exiting by user request.")
            sys.exit(0)
        except Exception:  # catch *all* exceptions
            LOGGER.error("Fatal error in main loop", exc_info=True)
            sys.exit(1)
        finally:
            LOGGER.info("es-writer was stopped")


if __name__ == "__main__":
    main()
