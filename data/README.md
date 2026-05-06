# Data directory

This directory is used to store application and user data that is excluded from code versioning as it can become quite large.

It used by:
* Postgres database: `data/postgres_data/`
* Elasticsearch index: `data/es_data/`

You can add your own data for use by your application:
* `data/mydata1/`
* `data/mydata2/`
