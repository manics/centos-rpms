#!/bin/bash
#
# /etc/init.d/omero
# Subsystem file for "omero" server
#
### BEGIN INIT INFO
# Provides:             omero-web
# Required-Start:       $local_fs $remote_fs $network $time omero postgresql
# Required-Stop:        $local_fs $remote_fs $network $time omero postgresql
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short-Description:    OMERO.web
### END INIT INFO
# chkconfig: - 90 10
# description: OMERO.web

# Source function library.
. /etc/rc.d/init.d/functions

RETVAL=0
prog="omero-web"

# Read configuration variable file if it is present
[ -r /etc/default/$prog ] && . /etc/default/$prog
# also read the omero config
[ -r /etc/default/omero ] && . /etc/default/omero

OMERO_HOME="/opt/omero44/server"
OMERO_USER="omero"

start() {	
	echo -n $"Starting $prog: "
	runuser ${OMERO_USER} -c "${OMERO_HOME}/bin/omero web start" &> \
		/dev/null && echo -n ' OMERO.web'
	#runuser ${OMERO_USER} -c \
	#	"bash ${OMERO_HOME%OMERO.server}/nginx-control.sh start"
	RETVAL=$?
	[ "$RETVAL" = 0 ] && echo_success || echo_failure
	echo
}

stop() {
	echo -n $"Stopping $prog: "
	runuser ${OMERO_USER} -c "${OMERO_HOME}/bin/omero web stop" &> \
		/dev/null && echo -n ' OMERO.web'
	#runuser ${OMERO_USER} -c \
	#	"bash ${OMERO_HOME%OMERO.server}/nginx-control.sh stop"
	RETVAL=$?
	[ "$RETVAL" = 0 ] && echo_success || echo_failure
	echo
}

status() {
	echo -n $"Status $prog: "
	runuser ${OMERO_USER} -c "${OMERO_HOME}/bin/omero web status"
	#runuser ${OMERO_USER} -c \
	#	"bash ${OMERO_HOME%OMERO.server}/nginx-control.sh status"
	RETVAL=$?
	echo
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	restart)
		stop
		start
		;;
	status)
		status
		RETVAL=$?
		;;
	*)	
		echo $"Usage: $0 {start|stop|restart|status}"
		RETVAL=1
esac
exit $RETVAL
