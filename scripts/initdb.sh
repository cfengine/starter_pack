#!/usr/bin/env bash
echo "=============================== POSTGRES ==============================="

echo "Giving root user access to postgres"
( cd / && sudo -u postgres createuser --login --superuser root )

echo "Starting postgres"
service postgresql start

echo "Creating databases"
createdb cfdb
createdb cfsettings

echo "Initializing DB schemas"
base_dir='/northern.tech/cfengine'
psql -d cfdb -f $base_dir/nova/db/schema.sql > /dev/null 2>&1
# psql -d cfdb -f $base_dir/mission-portal/phpcfenginenova/cfdb_import.sql > /dev/null 2>&1

psql -d cfsettings -f $base_dir/nova/db/schema_settings.sql > /dev/null 2>&1
psql -d cfsettings -f $base_dir/nova/db/ootb_settings.sql > /dev/null 2>&1
psql -d cfsettings -f $base_dir/nova/db/cfsettings-setadminpassword.sql > /dev/null 2>&1
