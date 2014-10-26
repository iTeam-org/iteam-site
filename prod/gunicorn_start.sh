#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

WORKINGDIR=/home/nodraak/Telechargements/iteam.org/

LOGFILE=$WORKINGDIR/gunicorn.log
ERRFILE=$WORKINGDIR/gunicorn_err.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3 # how many worker processes : should be nb_cpu*2+1
USER=nodraak
GROUP=nodraak

cd $WORKINGDIR
exec ../bin/gunicorn iTeam.wsgi:application \
-b localhost:8000 \
--timeout=300 \
--workers $NUM_WORKERS \
--name $NAME \
--user=$USER \
--group=$GROUP \
--log-level=debug \
--log-file=$LOGFILE 2>>$ERRFILE
