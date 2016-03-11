#!/usr/bin/env bash

#
# ==================================================
# Provision shell script for X Django project
# ==================================================
#

SCRIPT=$(readlink -f "$0")
SCRIPT_PATH=$(dirname "$SCRIPT")
PROJECT_PATH=$SCRIPT_PATH/..
PACKAGE_NAME=equinox_spring16_api
PACKAGE_PATH=$PROJECT_PATH/equinox_spring16_api
PROVISION_RENDER=$PROJECT_PATH/deployment_tools/provision_render.py


update_apt_get () {
    sudo apt-get -y update
}

install_if_not_installed () {
    for prog in $@
    do
        echo "Installing $prog ..."
        output=$(apt-cache policy $prog)
        #echo $output
        if test "${output#*Installed: (none)}" != "$output"; then
            sudo apt-get update
            sudo apt-get -y install $prog
        else
            echo "$prog was already installed"
        fi
    done
}

install_project_dependencies () {
    install_if_not_installed git build-essential python-dev python-setuptools python-pip python-virtualenv \
    libjpeg-dev libpng12-dev python-imaging postgresql postgresql-contrib libpq-dev supervisor nginx

    test -f /usr/lib/libfreetype.so || sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
    test -f /usr/lib/libjpeg.so || sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
    test -f /usr/lib/libz.so || sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/
}

create_user_group () {
    USER=$1
    GROUP=$2

    echo 'Creating user/group ...'
    sudo groupadd --system $GROUP
    sudo useradd --system --gid $GROUP --shell /bin/bash --home /webapps/$USER $USER

    echo 'Making user directory ...'
    test -d /webapps/$USER || sudo mkdir -p /webapps/$USER
    sudo chown $USER:$GROUP /webapps/$USER
}

create_and_provision_virtualenv () {
    USER=$1

    echo 'Creating virtualenv ...'
    test -f /webapps/$USER/bin/python || sudo su $USER -c "virtualenv /webapps/$USER"

    PIP=/webapps/$USER/bin/pip

    echo 'Installing pip dependencies ...'
    sudo $PIP install psycopg2==2.6.1
    sudo $PIP install Django==1.9.4
    sudo $PIP install djangorestframework==3.3.2
    sudo $PIP install pillow==3.0.0
    sudo $PIP install gunicorn==19.3.0
    sudo $PIP install setproctitle==1.1.9
    sudo $PIP install xdjango==0.2
    sudo $PIP install django-extra-fields==0.5
    sudo $PIP install djangorestframework-camel-case==0.2.0
    sudo $PIP install django-rest-swagger==0.3.5
}

copy_and_set_up_django_project () {
    USER=$1
    SERVER_NAME=$2
    DB_NAME=$3
    DB_PASSWORD=$4
    DEBUG=$5

    DEST_DIR=/webapps/$USER/$PACKAGE_NAME
    MEDIA_DIR=/webapps/$USER/var/media/
    STATIC_FROM_DIR=/webapps/$USER/$PACKAGE_NAME/static
    STATIC_DEST_DIR=/webapps/$USER/var/static
    SETTINGS_FILE=/webapps/$USER/$PACKAGE_NAME/$PACKAGE_NAME/settings.py

    echo 'Copying project directory to destination folder ...'
    test -d $DEST_DIR && sudo rm -R $DEST_DIR
    sudo su $USER -c "cp -R $PACKAGE_PATH $DEST_DIR"

    echo 'Moving static directory ...'
    test -d $STATIC_DEST_DIR && rm -R $STATIC_DEST_DIR
    sudo su $USER -c "cp -R $STATIC_FROM_DIR $STATIC_DEST_DIR"
    rm -R $STATIC_FROM_DIR

    echo 'Creating media directory ...'
    test -d $MEDIA_DIR || sudo su $USER -c "mkdir -p $MEDIA_DIR"

    # Set settings.py file
    sudo su $USER -c "python $PROVISION_RENDER settings $MEDIA_DIR $STATIC_DEST_DIR $SERVER_NAME $DB_NAME $USER $DB_PASSWORD $DEBUG $PACKAGE_NAME > $SETTINGS_FILE"

}

set_up_gunicorn_supervisor () {
    USER=$1
    GROUP=$2
    PROGRAM=$3
    SETTINGS_FILE=$4

    SOCKFILE=/webapps/$USER/run/gunicorn.sock
    RUNDIR=$(dirname $SOCKFILE)
    LOG_FILE=/webapps/$USER/logs/gunicorn_supervisor.log
    LOGDIR=$(dirname $LOG_FILE)
    START_SCRIPT=/webapps/$USER/bin/gunicorn_start.sh
    DJANGO_PROJECT_DIR=/webapps/$USER/$PACKAGE_NAME/
    ACTIVATE_VIRTUALENV=/webapps/$USER/bin/activate
    SUPERVISOR_CONF=/etc/supervisor/conf.d/$PROGRAM.conf

    echo 'Setting up gunicorn ...'
    sudo su $USER -c "python $PROVISION_RENDER gunicorn_start $PROGRAM $DJANGO_PROJECT_DIR $SOCKFILE $LOG_FILE $USER $GROUP $ACTIVATE_VIRTUALENV $PACKAGE_NAME > $START_SCRIPT"
    sudo su $USER -c "chmod a+x $START_SCRIPT"

    echo 'Setting up supervisor ...'
    sudo su $USER -c "test -d $RUNDIR || mkdir -p $RUNDIR"
    sudo su $USER -c "test -d $LOGDIR || mkdir -p $LOGDIR"
    sudo su $USER -c "test -f $LOGFILE || touch $LOGFILE"

    sudo python $PROVISION_RENDER supervisor $PROGRAM $START_SCRIPT $USER $LOG_FILE > $SUPERVISOR_CONF

    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl restart $PROGRAM
}

set_up_nginx () {
    USER=$1
    PROGRAM=$2
    SERVER_NAME=$3
    PORT=$4

    SOCKFILE=/webapps/$USER/run/gunicorn.sock
    LOGDIR=/webapps/$USER/logs
    ACCESS_LOGFILE=$LOGDIR/nginx-access.log
    ERROR_LOGFILE=$LOGDIR/nginx-error.log
    STATIC=/webapps/$USER/var/static/
    MEDIA=/webapps/$USER/var/media/
    NGINX_SITE_NAME=nginx-site-$PROGRAM

    echo 'Setting up nginx ...'
    sudo su $USER -c "test -d $LOGDIR || mkdir -p $LOGDIR"
    sudo su $USER -c "test -f $ACCESS_LOGFILE || touch $ACCESS_LOGFILE"
    sudo su $USER -c "test -f $ERROR_LOGFILE || touch $ERROR_LOGFILE"

    sudo python $PROVISION_RENDER nginx $PROGRAM $SOCKFILE $PORT $SERVER_NAME $ACCESS_LOGFILE $ERROR_LOGFILE $STATIC $MEDIA > /etc/nginx/sites-available/$NGINX_SITE_NAME

    test -f /etc/nginx/sites-enabled/$NGINX_SITE_NAME && sudo rm /etc/nginx/sites-enabled/$NGINX_SITE_NAME
    sudo ln -s /etc/nginx/sites-available/$NGINX_SITE_NAME /etc/nginx/sites-enabled/$NGINX_SITE_NAME
    sudo service nginx restart
}

create_postgres_db () {
    USER=$1
    DATA_BASE_NAME=$2
    DB_PASSWORD=$3

    PYTHON=/webapps/$USER/bin/python
    MANAGE_PY=/webapps/$USER/$PACKAGE_NAME/manage.py
    DEST_DIR=/webapps/$USER/$PACKAGE_NAME

    echo 'Creating postgres db ...'
    sudo su postgres -c "createuser -s -r $USER > /dev/null 2>&1"
    sudo su postgres -c "psql -c \"ALTER USER $USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';\" > /dev/null 2>&1"
    sudo su $USER -c "createdb $DATA_BASE_NAME > /dev/null 2>&1"

    synchronize_and_migrate_db $USER
}

synchronize_and_migrate_db () {
    USER=$1

    PYTHON=/webapps/$USER/bin/python
    MANAGE_PY=/webapps/$USER/$PACKAGE_NAME/manage.py
    DEST_DIR=/webapps/$USER/$PACKAGE_NAME/

    echo 'Synchronizating and migrating data base ...'
    cd $DEST_DIR
    sudo su $USER -c "$PYTHON $MANAGE_PY migrate"
}



## Main

if [ "$1" = "devel" ]; then
    USER=equinox_api_dev
    GROUP=webapps
    APP=equinox_api_dev
    SERVER_NAME=api.spring16.equinox.local
    SERVER_PORT=80
    DATA_BASE_NAME=sqldb
    DB_PASSWORD=password
    DEBUG=True

    install_project_dependencies
    create_user_group $USER $GROUP
    create_and_provision_virtualenv $USER
    copy_and_set_up_django_project $USER $SERVER_NAME $DATA_BASE_NAME $DB_PASSWORD $DEBUG
    create_postgres_db $USER $DATA_BASE_NAME $DB_PASSWORD
    set_up_gunicorn_supervisor $USER $GROUP $APP
    set_up_nginx $USER $APP $SERVER_NAME $SERVER_PORT

else
    echo "Usage: $0 devel"
fi