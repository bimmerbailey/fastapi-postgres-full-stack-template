#!/bin/bash
set -e

echo "Creating Test Database"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE your_app;
	CREATE DATABASE test_your_app;
EOSQL