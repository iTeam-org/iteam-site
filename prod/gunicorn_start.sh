#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

NAME="iTeam"
WORKINGDIR=/home/nodraak/Telechargements/iteam.org/

LOGFILE=$WORKINGDIR/gunicorn.log
ERRFILE=$WORKINGDIR/gunicorn_err.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3 # how many worker processes : should be nb_cpu*2+1
# SOCKFILE=/home/nodraak/Telechargements/iteam.org/gunicorn.sock
USER=nodraak
GROUP=nodraak

echo "Starting gunicorn server for $NAME"

cd $WORKINGDIR
exec gunicorn wsgi:application \
-b localhost:8000 \
#--bind=unix:$SOCKFILE
--timeout=300 \
--workers $NUM_WORKERS \
--name $NAME \
--user=$USER \
--group=$GROUP \
--log-level=debug \
--log-file=$LOGFILE 2>>$ERRFILE
