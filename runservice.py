#!/usr/bin/python

from os import environ
#from flask import Flask
from gevent import pywsgi
from whmgsystem import app
from whmgsystem.syslog import systemlog
from whmgsystem.conf import initsystem
if __name__ == '__main__':
    HOST = "0.0.0.0"
    try:
        PORT = int(environ.get('SERVER_PORT', '5554'))
    except ValueError:
        PORT = 5554
    app.secret_key = 'sjflw2332l#$@^!@fsfds'
    app.logger.addHandler(systemlog.log_init())
    app.debug=True
    initsystem.init_system()
    server = pywsgi.WSGIServer((HOST, PORT), app)
    server.serve_forever()