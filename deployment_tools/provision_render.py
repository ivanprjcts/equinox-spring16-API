import os
import sys


DIR_PATH = os.path.dirname(os.path.abspath(__file__))

GUNICORN_START_TEMPLATE = DIR_PATH + "/gunicorn_start.sh.template"
SUPERVISOR_CONF_TEMPLATE = DIR_PATH + "/supervisor_conf.template"
NGINX_TEMPLATE = DIR_PATH + "/x-nginx-site.template"
SETTINGS_TEMPLATE = DIR_PATH + "/settings.py.template"


def render_gunicorn_start(program, django_project_dir, sockfile, logfile, user, group, activate_virtenv, package_name):
    f = open(GUNICORN_START_TEMPLATE, "r")
    template = f.read()
    f.close()

    template = template.replace("REPLACE_PROGRAM_HERE", program)
    template = template.replace("REPLACE_DJANGO_PROJECT_DIR_HERE", django_project_dir)
    template = template.replace("REPLACE_RUN_SOCK_FILE_HERE", sockfile)
    template = template.replace("REPLACE_LOG_FILE_HERE", logfile)
    template = template.replace("REPLACE_USER_HERE", user)
    template = template.replace("REPLACE_GROUP_HERE", group)
    template = template.replace("REPLACE_VIRTUALENV_ACTIVATE_HERE", activate_virtenv)
    template = template.replace("REPLACE_PACKAGE_NAME_HERE", package_name)
    return template


def render_supervisor_conf(program, gunicorn_start_script, user, logfile):
    f = open(SUPERVISOR_CONF_TEMPLATE, "r")
    template = f.read()
    f.close()

    template = template.replace("REPLACE_PROGRAM_HERE", program)
    template = template.replace("REPLACE_GUNICORN_START_SCRIPT_HERE", gunicorn_start_script)
    template = template.replace("REPLACE_USER_HERE", user)
    template = template.replace("REPLACE_GUNICORN_LOG_FILE_HERE", logfile)
    return template


def render_nginx(program, sockfile, port, server_name, access_log, error_log, static_loc, media_loc):
    f = open(NGINX_TEMPLATE, "r")
    template = f.read()
    f.close()

    template = template.replace("REPLACE_SERVER_APP_HERE", program)
    template = template.replace("REPLACE_SOCKFILE_HERE", sockfile)
    template = template.replace("REPLACE_LISTEN_PORT_HERE", port)
    template = template.replace("REPLACE_SERVER_NAME_HERE", server_name)
    template = template.replace("REPLACE_ACCESS_LOG_FILE_HERE", access_log)
    template = template.replace("REPLACE_ERROR_LOG_FILE_HERE", error_log)
    template = template.replace("REPLACE_STATIC_LOCATION_HERE", static_loc)
    template = template.replace("REPLACE_MEDIA_LOCATION_HERE", media_loc)
    return template


def render_settings(media_root, static_root, allowed_hosts, db_name, db_user, db_password, debug, package_name):
    f = open(SETTINGS_TEMPLATE, "r")
    template = f.read()
    f.close()

    template = template.replace("REPLACE_MEDIA_ROOT_HERE", media_root)
    template = template.replace("REPLACE_STATIC_ROOT_HERE", static_root)
    template = template.replace("REPLACE_ALLOWED_HOSTS_HERE", allowed_hosts)
    template = template.replace("REPLACE_DB_NAME_HERE", db_name)
    template = template.replace("REPLACE_DB_USER_HERE", db_user)
    template = template.replace("REPLACE_DB_PASSWORD_HERE", db_password)
    template = template.replace("REPLACE_DEBUG_HERE", debug)
    template = template.replace("REPLACE_PACKAGE_NAME_HERE", package_name)
    return template


if __name__ == '__main__':

    if len(sys.argv) == 10 and sys.argv[1] == "gunicorn_start":
        program = sys.argv[2]
        django_dir = sys.argv[3]
        sockfile = sys.argv[4]
        logfile = sys.argv[5]
        user = sys.argv[6]
        group = sys.argv[7]
        activate = sys.argv[8]
        package_name = sys.argv[9]
        gunicorn_start = render_gunicorn_start(program, django_dir, sockfile, logfile, user, group, activate,
                                               package_name)
        print(gunicorn_start)
    elif len(sys.argv) == 10 and sys.argv[1] == "nginx":
        program = sys.argv[2]
        sockfile = sys.argv[3]
        port = sys.argv[4]
        server_name = sys.argv[5]
        access_log = sys.argv[6]
        error_log = sys.argv[7]
        static_loc = sys.argv[8]
        media_loc = sys.argv[9]
        nginx = render_nginx(program, sockfile, port, server_name, access_log, error_log, static_loc, media_loc)
        print(nginx)
    elif len(sys.argv) == 6 and sys.argv[1] == "supervisor":
        program = sys.argv[2]
        gunicorn_start_script = sys.argv[3]
        user = sys.argv[4]
        logfile = sys.argv[5]
        supervisor_conf = render_supervisor_conf(program, gunicorn_start_script, user, logfile)
        print(supervisor_conf)
    elif len(sys.argv) == 10 and sys.argv[1] == "settings":
        media_root = sys.argv[2]
        static_root = sys.argv[3]
        allowed_hosts = sys.argv[4]
        db_name = sys.argv[5]
        db_user = sys.argv[6]
        db_password = sys.argv[7]
        debug = sys.argv[8]
        package_name = sys.argv[9]
        settings_py = render_settings(media_root, static_root, allowed_hosts, db_name, db_user, db_password, debug, package_name)
        print(settings_py)
    else:
        print("USAGE: %s gunicorn_start PROGRAM DJANGO_PRJ_DIR SOCKFILE LOGFILE USER GROUP ACTIVATE_BIN PACKAGE_NAME" % sys.argv[0])
        print("       %s supervisor PROGRAM GUNICORN_START_SCRIPT USER LOGFILE" % sys.argv[0])
        print("       %s nginx PROGRAM SOCKFILE PORT SERVER_NAME ACCESS_LOG ERR_LOG STATIC_LOC MEDIA_LOC" % sys.argv[0])
        print("       %s settings MEDIA_ROOT ALLOWED_HOSTS DB_NAME DB_USER DB_PASSWORD DEBUG" % sys.argv[0])