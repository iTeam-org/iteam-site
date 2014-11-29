#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

WORKINGDIR=/opt/iteam-env/iteam-site/

LOGFILE=$WORKINGDIR/../log/gunicorn.log
ERRFILE=$WORKINGDIR/../log/gunicorn_err.log
NUM_WORKERS=3 # how many worker processes : should be nb_cpu*2+1
USER=iteam
GROUP=iteam

cd $WORKINGDIR
exec ../bin/gunicorn iTeam.wsgi:application \
-b localhost:8000 \
--timeout=300 \
--workers $NUM_WORKERS \
--name=iTeam \
--user=$USER \
--group=$GROUP \
--log-level=debug \
--log-file=$LOGFILE 2>>$ERRFILE
