#!/bin/bash
#
# /etc/init.d/omero
# Subsystem file for "omero" server
#
### BEGIN INIT INFO
# Provides:             omero
# Required-Start:       $local_fs $remote_fs $network $time postgresql
# Required-Stop:        $local_fs $remote_fs $network $time postgresql
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short-Description:    OMERO.server
### END INIT INFO
# chkconfig: - 85 15
# description: OMERO.server

# Source function library.
. /etc/rc.d/init.d/functions

RETVAL=0
prog="omero"

# Read configuration variable file if it is present
[ -r /etc/default/$prog ] && . /etc/default/$prog

OMERO_HOME="/opt/omero/server"
OMERO_USER="omero"

start() {	
	echo -n $"Starting $prog: "
	runuser ${OMERO_USER} -c "${OMERO_HOME}/bin/omero admin start" &> \
		/dev/null && echo -n ' OMERO.server'
	RETVAL=$?
	[ "$RETVAL" = 0 ] && echo_success || echo_failure
	echo
}

stop() {
	echo -n $"Stopping $prog: "
	runuser ${OMERO_USER} -c "${OMERO_HOME}/bin/omero admin stop" &> \
		/dev/null && echo -n ' OMERO.server'
	RETVAL=$?
	[ "$RETVAL" = 0 ] && echo_success || echo_failure
	echo
}

status() {
	echo -n $"Status $prog: "
	runuser ${OMERO_USER} -c "${OMERO_HOME}/bin/omero admin status" && \
		echo -n ' OMERO.server running' || \
		echo -n ' OMERO.server not running'
	RETVAL=$?
	echo
}

diagnostics() {
	echo -n $"Diagnostics $prog: "
	runuser ${OMERO_USER} -c "${OMERO_HOME}/bin/omero admin diagnostics"
	RETVAL=$?
	echo
}

clearlogs() {
	LOGDIR=${LOGDIR:-${OMERO_HOME}/var/log}
	TARFILE=${TARFILE:-omero-logs-$(date '+%F').tar.bz2}
	echo -n $"Clearing logs $prog:"
	cd $LOGDIR && tar -caf $TARFILE *.{err,out,log} && \
		(for x in ${LOGDIR}/*.{err,out,log}; do : > $x ;done) && \
		chown $OMERO_USER ${LOGDIR}/${TARFILE} && \
		echo -n $" saved to $LOGFILE/$TARFILE:"
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
	diagnostics)
		diagnostics
		RETVAL=$?
		;;
	clearlogs)
		clearlogs
		RETVAL=$?
		;;
	*)	
		echo $"Usage: $0 {start|stop|restart|status|diagnostics|clearlogs}"
		RETVAL=1
esac
exit $RETVAL
