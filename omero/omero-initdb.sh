#!/bin/sh
# OMERO database initialisation script

OMERO_HOME=/opt/omero44/server
OMERO_DATA_DIR=/OMERO
PGCONFIG=/var/lib/pgsql/data/pg_hba.conf

if [ "$(ls -A $OMERO_DATA_DIR)" ]; then
	echo -n "Data directory is not empty, aborting."
	exit 2
fi

# Configure PostgreSQL to use md5 password authentication (this assumes
# PostgreSQL is already running):
grep -E '^\s*host\s+omero\s+omero+\s+127.0.0.1/32+\s+md5\s*$' $PGCONFIG > /dev/null
if [ $? -ne 0 ]; then
	sed -i.omero '0,/^host.*/s//'\
'host    omero       omero       127.0.0.1\/32          md5\n'\
'host    omero       omero       ::1\/128               md5\n&/' \
	$PGCONFIG
	service postgresql reload
fi

# Create a random password
DBPASS=`LC_CTYPE=C tr -dc "[:alpha:]" < /dev/urandom | head -c 8`

# Create a database user (this will prompt for a database password) and
# database:
#su - postgres -c "createuser -DRSP omero"
su - postgres -c \
	"psql -c \"CREATE ROLE omero WITH LOGIN ENCRYPTED PASSWORD '$DBPASS';\""
su - postgres -c "createdb -E UTF8 -O omero omero"
if [ $? -ne 0 ]; then
	# If the previous line fails then try:
	su - postgres -c "createdb -E UTF8 -T template0 -O omero omero"
fi
su - postgres -c "createlang plpgsql omero"

# Configure OMERO:
su - omero -c "$OMERO_HOME/bin/omero config set omero.db.name omero"
su - omero -c "$OMERO_HOME/bin/omero config set omero.db.user omero"
su - omero -c "$OMERO_HOME/bin/omero config set omero.db.pass $DBPASS"

# Setup the database:
pushd $OMERO_HOME/var
su - omero -c "$OMERO_HOME/bin/omero db script '' '' omero"
su - omero -c \
	"PGPASSWORD=$DBPASS psql -hlocalhost -Uomero omero < OMERO4.4__0.sql"
popd

# Enable automatic startup:
chkconfig omero on
#chkconfig omero-web on

