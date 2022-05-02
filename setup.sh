#!/usr/bin/env bash
docker run -d \
	--name kosha-postgres \
	-e POSTGRES_PASSWORD=kosha \
	-v ${HOME}/postgres-data/:/var/lib/postgresql/data \
        -p 5432:5432 \
        postgres

docker run \
--detach \
--name=kosha-mysql \
--env="MYSQL_ROOT_PASSWORD=kosha" \
--publish 6603:3306 \
--volume=${HOME}/mysql-data/:/var/lib/mysql \
mysql

docker run -d -p 27017:27017 --name kosha-mongodb -v /Users/pasudhee/dev/kosha/mongodb_data:/data/db mongo

docker run -d -it -p 3000:3000 huginn/huginn

DATABASE=postgresql DB_USER=postgres DB_PASSWORD=kosha DB_SERVER=localhost DB_NAME=postgres uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8001

DATABASE=mysql DB_USER=root DB_PASSWORD=kosha DB_SERVER=localhost DB_NAME=kosha uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8001å