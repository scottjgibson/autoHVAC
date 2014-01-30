from time import time, sleep, localtime, strftime
import logging

class DS18B20(object):

  def __init__(self, name, path):
    self.name = name
    self.sensor_path = path
    self.reties = 3
    self.currentTemp = None
    self.log = logging.getLogger(__name__ + self.name)
    self.log.info('DS18B20 Object Initialized') 

  def read_temp_raw(self):
      f = open(self.sensor_path, 'r')
      lines = f.readlines()
      f.close()
      self.log.debug(lines) 
      return lines

  def read_temp(self):
    for retry in range(self.reties):
      lines = self.read_temp_raw()
      if (lines[0].strip()[-3:] == 'YES'):
        break
      sleep(0.2)


    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      self.currentTemp = float(temp_string) / 1000.0
      self.log.info("Current Temp: %d degC"%self.currentTemp) 
      return self.currentTemp
    else:
      self.log.error("Failed to read temperature") 
      return None

if __name__ == "__main__":
  import logging.config
  logging.basicConfig(level=logging.INFO)
  sensor1 = DS18B20("sensor1", "/sys/bus/w1/devices/10-000801d42949/w1_slave")
  sensor1.read_temp()


