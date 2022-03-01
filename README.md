# Elasticsearch cluster in docker

This project provides you with an elasticsearch cluster consisting of three elasticsearch instances, using the basic license. I've created it during and after the Elastic Engineer training to help me with a ready-to-go environment where I can play with the training labs.

Disclaimer: this setup is not meant for production usage!

Note: this example was extended to add TLS and RBAC to the cluster and its clients. This has been inspired by the example [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker-compose-file).

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

Confirm that elasticsearch is healthy (after a little while) by visiting one of the following links from your browser or a tool like curl or [httpie](https://httpie.org/):

Elastic search nodes:

- [cluster health](http://localhost:9200/_cluster/health?pretty=true)
- [cluster nodes](http://localhost:9200/_nodes/_all/http?pretty=true)
- [elasticsearch1 node health](http://localhost:9200/_cat/health)
- [elasticsearch2 node health](http://localhost:9201/_cat/health)
- [elasticsearch3 node health](http://localhost:9202/_cat/health)

Other services:

- [Kibana](http://localhost:5601)
- [All five indices in Kibana](http://localhost:5601/app/kibana#/management/elasticsearch/index_management/indices?_g=())

## (Optional) Setup security features for Elasticsearch

By default, the Elasticsearch security features are disabled when you have a basic or trial license. To enable security features, use the xpack.security.enabled setting..

_Starting with Elastic Stack 6.8 and 7.1, security features like TLS encrypted communication, role-based access control (RBAC), and more are available for free within the default distribution. In this blog post, we’re going to cover how to get started with using these features to secure your Elasticsearch clusters._

[(source)](https://www.elastic.co/blog/getting-started-with-elasticsearch-security)

## Snapshots

A folder has been bind-mounted to all elasticsearch nodes already with the purpose of sharing snapshots with the docker host. This folder is relative from this directory: `./shared_folder`.
When registering a (fs-type) snapshot repository inside elasticsearch, you should make it point to `/shared_folder` from inside the container.

## Add SSL/TLS support

    docker run -it docker.elastic.co/elasticsearch/elasticsearch:8.0.0 /bin/bash
    ./bin/elasticsearch-certutil http


    elasticsearch@b0cf0c731dc4:~$ ./bin/elasticsearch-certutil http

    ## Elasticsearch HTTP Certificate Utility

    The 'http' command guides you through the process of generating certificates
    for use on the HTTP (Rest) interface for Elasticsearch.

    This tool will ask you a number of questions in order to generate the right
    set of files for your needs.

    ## Do you wish to generate a Certificate Signing Request (CSR)?

    A CSR is used when you want your certificate to be created by an existing
    Certificate Authority (CA) that you do not control (that is, you don't have
    access to the keys for that CA). 

    If you are in a corporate environment with a central security team, then you
    may have an existing Corporate CA that can generate your certificate for you.
    Infrastructure within your organisation may already be configured to trust this
    CA, so it may be easier for clients to connect to Elasticsearch if you use a
    CSR and send that request to the team that controls your CA.

    If you choose not to generate a CSR, this tool will generate a new certificate
    for you. That certificate will be signed by a CA under your control. This is a
    quick and easy way to secure your cluster with TLS, but you will need to
    configure all your clients to trust that custom CA.

    Generate a CSR? [y/N]N

    ## Do you have an existing Certificate Authority (CA) key-pair that you wish to use to sign your certificate?

    If you have an existing CA certificate and key, then you can use that CA to
    sign your new http certificate. This allows you to use the same CA across
    multiple Elasticsearch clusters which can make it easier to configure clients,
    and may be easier for you to manage.

    If you do not have an existing CA, one will be generated for you.

    Use an existing CA? [y/N]N
    A new Certificate Authority will be generated for you

    ## CA Generation Options

    The generated certificate authority will have the following configuration values.
    These values have been selected based on secure defaults.
    You should not need to change these values unless you have specific requirements.

    Subject DN: CN=Elasticsearch HTTP CA
    Validity: 5y
    Key Size: 2048

    Do you wish to change any of these options? [y/N]N

    ## CA password

    We recommend that you protect your CA private key with a strong password.
    If your key does not have a password (or the password can be easily guessed)
    then anyone who gets a copy of the key file will be able to generate new certificates
    and impersonate your Elasticsearch cluster.

    IT IS IMPORTANT THAT YOU REMEMBER THIS PASSWORD AND KEEP IT SECURE

    CA password:  [<ENTER> for none]
    Repeat password to confirm: 

    ## How long should your certificates be valid?

    Every certificate has an expiry date. When the expiry date is reached clients
    will stop trusting your certificate and TLS connections will fail.

    Best practice suggests that you should either:
    (a) set this to a short duration (90 - 120 days) and have automatic processes
    to generate a new certificate before the old one expires, or
    (b) set it to a longer duration (3 - 5 years) and then perform a manual update
    a few months before it expires.

    You may enter the validity period in years (e.g. 3Y), months (e.g. 18M), or days (e.g. 90D)

    For how long should your certificate be valid? [5y] 

    ## Do you wish to generate one certificate per node?

    If you have multiple nodes in your cluster, then you may choose to generate a
    separate certificate for each of these nodes. Each certificate will have its
    own private key, and will be issued for a specific hostname or IP address.

    Alternatively, you may wish to generate a single certificate that is valid
    across all the hostnames or addresses in your cluster.

    If all of your nodes will be accessed through a single domain
    (e.g. node01.es.example.com, node02.es.example.com, etc) then you may find it
    simpler to generate one certificate with a wildcard hostname (*.es.example.com)
    and use that across all of your nodes.

    However, if you do not have a common domain name, and you expect to add
    additional nodes to your cluster in the future, then you should generate a
    certificate per node so that you can more easily generate new certificates when
    you provision new nodes.

    Generate a certificate per node? [y/N]N

    ## Which hostnames will be used to connect to your nodes?

    These hostnames will be added as "DNS" names in the "Subject Alternative Name"
    (SAN) field in your certificate.

    You should list every hostname and variant that people will use to connect to
    your cluster over http.
    Do not list IP addresses here, you will be asked to enter them later.

    If you wish to use a wildcard certificate (for example *.es.example.com) you
    can enter that here.

    Enter all the hostnames that you need, one per line.
    When you are done, press <ENTER> once more to move on to the next step.

    elasticsearch1
    elasticsearch2
    elasticsearch3
    elasticsearch4
    elasticsearch5

    You entered the following hostnames.

    - elasticsearch1
    - elasticsearch2
    - elasticsearch3
    - elasticsearch4
    - elasticsearch5

    Is this correct [Y/n]Y

    ## Which IP addresses will be used to connect to your nodes?

    If your clients will ever connect to your nodes by numeric IP address, then you
    can list these as valid IP "Subject Alternative Name" (SAN) fields in your
    certificate.

    If you do not have fixed IP addresses, or not wish to support direct IP access
    to your cluster then you can just press <ENTER> to skip this step.

    Enter all the IP addresses that you need, one per line.
    When you are done, press <ENTER> once more to move on to the next step.


    You did not enter any IP addresses.

    Is this correct [Y/n]Y

    ## Other certificate options

    The generated certificate will have the following additional configuration
    values. These values have been selected based on a combination of the
    information you have provided above and secure defaults. You should not need to
    change these values unless you have specific requirements.

    Key Name: elasticsearch1
    Subject DN: CN=elasticsearch1
    Key Size: 2048

    Do you wish to change any of these options? [y/N]N

    ## What password do you want for your private key(s)?

    Your private key(s) will be stored in a PKCS#12 keystore file named "http.p12".
    This type of keystore is always password protected, but it is possible to use a
    blank password.

    If you wish to use a blank password, simply press <enter> at the prompt below.
    Provide a password for the "http.p12" file:  [<ENTER> for none]

    ## Where should we save the generated files?

    A number of files will be generated including your private key(s),
    public certificate(s), and sample configuration options for Elastic Stack products.

    These files will be included in a single zip archive.

    What filename should be used for the output zip file? [/usr/share/elasticsearch/elasticsearch-ssl-http.zip] 

    Zip file written to /usr/share/elasticsearch/elasticsearch-ssl-http.zip
    elasticsearch@b0cf0c731dc4:~$ 

Now we need to also create certificates for inter-node communication:

    docker run -it --mount type=bind,source=$(pwd)/ssl,target=/ssl docker.elastic.co/elasticsearch/elasticsearch:8.0.0 /bin/bash
    ./bin/elasticsearch-certutil cert --ca /ssl/ca/ca.p12

    elasticsearch@6127a83b1001:~$ ./bin/elasticsearch-certutil cert --ca /ssl/ca/ca.p12 
    This tool assists you in the generation of X.509 certificates and certificate
    signing requests for use with SSL/TLS in the Elastic stack.

    The 'cert' mode generates X.509 certificate and private keys.
        * By default, this generates a single certificate and key for use
        on a single instance.
        * The '-multiple' option will prompt you to enter details for multiple
        instances and will generate a certificate and key for each one
        * The '-in' option allows for the certificate generation to be automated by describing
        the details of each instance in a YAML file

        * An instance is any piece of the Elastic Stack that requires an SSL certificate.
        Depending on your configuration, Elasticsearch, Logstash, Kibana, and Beats
        may all require a certificate and private key.
        * The minimum required value for each instance is a name. This can simply be the
        hostname, which will be used as the Common Name of the certificate. A full
        distinguished name may also be used.
        * A filename value may be required for each instance. This is necessary when the
        name would result in an invalid file or directory name. The name provided here
        is used as the directory name (within the zip) and the prefix for the key and
        certificate files. The filename is required if you are prompted and the name
        is not displayed in the prompt.
        * IP addresses and DNS names are optional. Multiple values can be specified as a
        comma separated string. If no IP addresses or DNS names are provided, you may
        disable hostname verification in your SSL configuration.


        * All certificates generated by this tool will be signed by a certificate authority (CA)
        unless the --self-signed command line option is specified.
        The tool can automatically generate a new CA for you, or you can provide your own with
        the --ca or --ca-cert command line options.


    By default the 'cert' mode produces a single PKCS#12 output file which holds:
        * The instance certificate
        * The private key for the instance certificate
        * The CA certificate

    If you specify any of the following options:
        * -pem (PEM formatted output)
        * -multiple (generate multiple certificates)
        * -in (generate certificates from an input file)
    then the output will be be a zip file containing individual certificate/key files

    Enter password for CA (/ssl/ca/ca.p12) : 
    Please enter the desired output file [elastic-certificates.p12]: 
    Enter password for elastic-certificates.p12 : 

    Certificates written to /usr/share/elasticsearch/elastic-certificates.p12

    This file should be properly secured as it contains the private key for 
    your instance.
    This file is a self contained file and can be copied and used 'as is'
    For each Elastic product that you wish to configure, you should copy
    this '.p12' file to the relevant configuration directory
    and then follow the SSL configuration instructions in the product guide.

    For client applications, you may only need to copy the CA certificate and
    configure the client to trust this certificate.
    elasticsearch@6127a83b1001:~$ cp elastic-certificates.p12 /ssl/
    ca/                         elasticsearch/              elasticsearch-ssl-http.zip  kibana/                     
    elasticsearch@6127a83b1001:~$ cp elastic-certificates.p12 /ssl

And we need to make sure curl can use the certs also:

    cd /ssl/ca
    openssl pkcs12 -in ca.p12 -out ca.key.pem -nocerts -nodes
    openssl pkcs12 -in ca.p12 -out ca.crt.pem -clcerts -nokeys

Test with

    curl --cacert ssl/ca/ca.crt.pem "https://elasticsearch1:9200/_xpack?pretty" -u elastic:pass123

Now we have to create users/passwords to enabled access

    docker exec -it elasticsearch1 /bin/bash
    # Deprecated:
    ./bin/elasticsearch-setup-passwords interactive --url https://elasticsearch1:9200

    # Password for elastic
    elasticsearch-reset-password -b -u elastic --url https://elasticsearch1:9200
    Password for the [elastic] user successfully reset.
    New value: ABK-Gjyf7qA12SC9U4S+

    # Password for kibana_system
    elasticsearch-reset-password -b -u kibana_system --url https://elasticsearch1:9200
    Password for the [kibana_system] user successfully reset.
    New value: rOtkKPBgIk+WNpfhu*zc

Add a specific user

    ./bin/elasticsearch-users useradd newelastic -p newelastic1 -r superuser

Change a use password:

    bin/elasticsearch-users passwd UserToChangePassword
