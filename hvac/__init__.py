from humidifier import Humidifier
import logging

class Hvac:
  status = None
  config = None
  log = None

  def __init__(self):
    self.status = 'unconfigured'
    self.log = logging.getLogger(__name__)
    self.log.info('HVAC Object Initialized') 

  def configure(self, configuration):
    self.log.info('HVAC Configure') 
    self.log.info(configuration) 
    self.status = 'Idle'
    if (configuration['humidifier_enabled']):
      self.humidifier = Humidifier()
        
  def update(self):
    self.status = 'Idle'
    self.log.info('HVAC Update') 

