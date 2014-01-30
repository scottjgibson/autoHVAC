import urllib2
import json
from time import sleep, localtime, strftime
from datetime import datetime, date
import sys
import logging

class Wunderground(object):

  def __init__(self, key, state, city, retries):
    self.name = "Wunderground"
    self.key = key
    self.state = state
    self.city = city
    self.retries = retries
    self.temperature = None
    self.longterm_average_temperature = None
    self.wind = None
    self.readTime = None
    self.log = logging.getLogger(__name__ + self.name)
    self.log.info('Wunderground Object Initialized') 

  def __str__(self):
    ret = "Name: %s" % self.name
    ret += "\nCity: %s State: %s\n" %(self.city, self.state)
    ret += "Current Temperature (DegC): %d Current Wind (kph): %d\n" %(self.temperature, self.wind)
    ret += "Long Term Average Temperature (next 3 days): %d\n" %(self.longterm_average_temperature)
    ret += "Late Updated: %s\n" % self.readTime.strftime("%Y-%m-%d %H:%M:%S")
    return ret


  def get_current_weather(self):
    #Get data from weather service
    #If exception occurs, retry a few times then quit
    for retry in range(self.retries):
      try:
        f = urllib2.urlopen('http://api.wunderground.com/api/' + self.key + '/geolookup/conditions/q/' + self.state + '/' + self.city + '.json')
        json_string = f.read()
        self.log.debug(json_string)
        parsed_json = json.loads(json_string)
        location = parsed_json['location']['city']
        self.wind = parsed_json['current_observation']['temp_c']
        self.temperature = parsed_json['current_observation']['wind_kph']
        self.log.info("Outdoor Temp(degC): %d Wind(kph):%d" % (self.temperature, self.wind))
        self.readTime = datetime.now()
        break
      except:
        e = sys.exc_info()[0]
        self.log.error("Errror getting temperature: %s" % e)
        self.temperature = None
        sleep(0.1)

    if (f != None):
      f.close()

  def get_forcast_weather(self):
    #Get data from weather service
    #If exception occurs, retry a few times then quit
    for retry in range(self.retries):
      try:
        f = urllib2.urlopen('http://api.wunderground.com/api/' + self.key + '/forecast/q/' + self.state + '/' + self.city + '.json')
        json_string = f.read()
#        self.log.debug(json_string)
        parsed_json = json.loads(json_string)
        temps = []
        for data in parsed_json['forecast']['simpleforecast']['forecastday']:
          if data['period'] > 1:
            self.log.debug( data['date']['weekday'])
            self.log.debug( data['high']['celsius'])
            self.log.debug( data['low']['celsius'])
            temps.append(int(data['high']['celsius']))
            temps.append(int(data['low']['celsius']))
            
        self.longterm_average_temperature = sum(temps) / float(len(temps))
        self.readTime = datetime.now()
        break
      except:
        e = sys.exc_info()[0]
        self.log.error("Errror getting temperature: %s" % e)
        sleep(0.1)

    if (f != None):
      f.close()

if __name__ == "__main__":
  import logging.config
  logging.basicConfig(level=logging.INFO)
  wu = Wunderground("95785342b13712d0", "Ontario", "Kanata", 1)
  while 1:
    wu.get_current_weather()
    wu.get_forcast_weather()
    print wu
    sleep(60)

