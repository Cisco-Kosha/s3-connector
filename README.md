# Kosha Amazon S3 Connector

Amazon S3 (Simple Storage Service) is a cloud-based object storage service that enables you to store and retrieve large amounts of data over the internet, using highly scalable, reliable, fast, and inexpensive data storage.

The Kosha Amazon S3 connector enables you to perform REST API operations from the Amazon S3 API in your Kosha workflow or custom application. 

## Useful Actions

You can use the Kosha Amazon S3 connector to manage S3 buckets and retrieve metrics.

Refer to the Kosha Amazon S3 connector [API specification](openapi.json) for details.

### Buckets

Buckets are the basic unit of storage in S3, storing and organizing data as objects. Use the S3 Buckets API to:

* Create buckets
* List buckets
* Save, delete, and list objects in buckets

### Metrics

The S3 Metrics API serves Prometheus metrics related to the performance and usage of your S3 buckets.

## Authentication

To authenticate when provisioning the Kosha Amazon S3 connector, you need your:

* AWS access key ID
* AWS secret access key
