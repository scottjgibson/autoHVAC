#!/usr/bin/python
"""
CherryPy WebServer starter.
"""

__author__    = 'Jovan Brakus <jovan@brakus.rs>'
__contact__   = 'jovan@brakus.rs'
__date__      = '31 May 2012'

import sys
import logging 
#Set logging handlers for the first time
import logconfig
import cherrypy
from cherrypy.process.plugins import Monitor
from configserver.tools.iniconfig import IniConfig, purge_config_dict, validate_config_dict

from configserver.web import ConfigServer
from hvac import Hvac

log = logging.getLogger(__name__)
webConfigServer = None
periodicTask = None
hvac = Hvac()

def configureHvac():
  global hvac
  log.info('Initializing HVAC System') 
  ini_config = IniConfig(current=True)
  hvac.configure(ini_config.to_dict())

def updateHvac():
  global hvac
  if hvac.status is 'unconfigured':
    configureHvac()
  else:
    hvac.update()

def main():
  global webConfigServer
  global periodicTask
  try:
    webConfigServer = ConfigServer()
    periodicTask = Monitor(cherrypy.engine, updateHvac, frequency=1)
    periodicTask.start()
    webConfigServer.start()
    return 0
  except:
    # Dump callstack to log and exit with -1
    log.exception('Unexpected exception occured.') 
    return -1
  
if __name__ == '__main__':
      sys.exit(main())

