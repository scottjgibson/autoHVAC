"""
CherryPy Config server settings module.
"""

__author__    = 'Scott Gibson <scottgibson@gmail.com>'
__contact__   = 'scottgibson@gmail.com'
__date__      = '28 Jan 2014'

CONFIG_FILENAME = "autoHVAC.ini"
WEBSERVER_HOST = '0.0.0.0'
WEBSERVER_PORT = 8080
USERS = {'cherrypy': '57ed5d98cce71967d508cb785aa76d2c23894347'} # SHA1 hash for 'cherrypy' 
LOG_DIR = 'logs'
TEMP_DIR = 'temp'
