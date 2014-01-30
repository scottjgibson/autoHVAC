import logging

class Humidifier:
    status = None
    setHumidity = None
    deadband = None
    currentHumidity = None

    def __init__(self):
        self.status = 'Idle'
        self.setHumidity = 0
        self.deadband = 0
        self.currentHumidity = 0
        self.log = logging.getLogger(__name__)
        self.log.info('Humidifier Object Initialized') 
        
    def start(self):
        self.status = 'Running'

    def update(self):
        self.status = 'Running'

