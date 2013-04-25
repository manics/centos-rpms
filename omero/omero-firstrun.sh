#!/bin/sh
# OMERO database initialisation script
# This assumes the server and web components have been installed

OMERO_HOME=/opt/omero/server
OMERO_DATA_DIR=/OMERO
PGCONFIG=/var/lib/pgsql/data/pg_hba.conf
FASTCGICONFIG=/etc/httpd/conf.d/fastcgi.conf

if [ "$(ls -A $OMERO_DATA_DIR)" ]; then
	echo -n "Data directory is not empty, aborting."
	exit 2
fi

if [ ! -f $PGCONFIG ]; then
	service postgresql initdb
	service postgresql start
fi

# Configure PostgreSQL to use md5 password authentication:
grep -E '^\s*host\s+omero\s+omero+\s+127.0.0.1/32+\s+md5\s*$' $PGCONFIG > /dev/null
if [ $? -ne 0 ]; then
	sed -i.omero '0,/^host.*/s//'\
'host    omero       omero       127.0.0.1\/32          md5\n'\
'host    omero       omero       ::1\/128               md5\n&/' \
	$PGCONFIG
	service postgresql reload
fi

# Create a random password:
DBPASS=`LC_CTYPE=C tr -dc "[:alpha:]" < /dev/urandom | head -c 8`

# Create a database user:
#su - postgres -c "createuser -DRSP omero"
su - postgres -c \
	"psql -c \"CREATE ROLE omero WITH LOGIN ENCRYPTED PASSWORD '$DBPASS';\""
su - postgres -c "createdb -E UTF8 -O omero omero"
if [ $? -ne 0 ]; then
	# If the previous command fails then try:
	su - postgres -c "createdb -E UTF8 -T template0 -O omero omero"
fi
if [ $? -ne 0 ]; then
	# If the previous command fails then try:
	su - postgres -c \
		"createdb -E UTF8 -l en_US.UTF-8 -T template0 -O omero omero"
fi
if [ $? -ne 0 ]; then
	echo "ERROR: Failed to create database, aborting"
	exit 2
fi
su - postgres -c "createlang plpgsql omero"

# Configure OMERO database connection:
su - omero -c "$OMERO_HOME/bin/omero config set omero.db.name omero"
su - omero -c "$OMERO_HOME/bin/omero config set omero.db.user omero"
su - omero -c "$OMERO_HOME/bin/omero config set omero.db.pass $DBPASS"

# Setup the database:
pushd $OMERO_HOME/var
su - omero -c "$OMERO_HOME/bin/omero db script '' '' omero"
su - omero -c \
	"PGPASSWORD=$DBPASS psql -hlocalhost -Uomero omero < OMERO4.4__0.sql"
popd

# Configure OMERO web:
su - omero -c \
	"$OMERO_HOME/bin/omero config set omero.web.application_server fastcgi-tcp"

# Remove the default FastCgi options
if [ -f "$FASTCGICONFIG" ]; then
	sed -i.omero 's/^\s*FastCgi/#&/' "$FASTCGICONFIG"
fi


echo "WARNING: OMERO root password set to 'omero', you should change this."

# Enable automatic startup:
echo "If this script has completed successfully you can start OMERO:"
echo "    service omero start"
echo "    service omero-web start"
echo "    service httpd start"
echo "Note postgresql should have been started by this script."
echo "To automatically run OMERO at system boot:"
echo "    chkconfig postgresql on"
echo "    chkconfig omero on"
echo "    chkconfig omero-web on"
echo "    chkconfig httpd on"



