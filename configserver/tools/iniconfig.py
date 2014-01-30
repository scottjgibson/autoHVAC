"""
Ini file configuration management functionality
"""
__author__    = 'Scott Gibson <scottgibson@gmail.com>'
__contact__   = 'scottgibson@gmail.com'
__date__      = '28 Jan 2014'

import os
import logging
import sys

from ConfigParser import SafeConfigParser
from configserver import settings

log = logging.getLogger(__name__)

class IniConfig:
    general = None
    tempodb = None
    plotly = None
    ds18b20_1 = None
    ds18b20_2 = None
    wunderground = None
    nest = None
    humidifier = None
        
    config_filepath = None
    
    def __init__(self, current = True, config_dict = None, update_normalization = False):
        ''' Config object constructor. Can create data from actual config file or from given config dictionary. '''
        #First we create empty config dicts.
        self.general = dict()
        self.tempodb = dict()
        self.plotly = dict()
        
        self.config_filepath = os.path.join(os.getcwd(), settings.CONFIG_FILENAME)
        print self.config_filepath
        #If set, read configuration from actual config file.
        if current:
            log.debug("Reading parameters from INI configuration file.")
    
            #Try to guess where is ini file
            if not os.path.exists(self.config_filepath):
                log.error("INI configuration file was not found.")
            
            parser = SafeConfigParser()
            parser.read(self.config_filepath)
            
            if parser.has_section('general'):
                self.general = dict(parser.items('general'))
            if parser.has_section('tempodb'):
                self.tempodb = dict(parser.items('tempodb'))
            if parser.has_section('plotly'):
                self.plotly = dict(parser.items('plotly'))
            if parser.has_section('ds18b20_1'):
                self.ds18b20_1 = dict(parser.items('ds18b20_1'))
            if parser.has_section('ds18b20_2'):
                self.ds18b20_2 = dict(parser.items('ds18b20_2'))
            if parser.has_section('wunderground'):
                self.wunderground = dict(parser.items('wunderground'))
            if parser.has_section('nest'):
                self.nest = dict(parser.items('nest'))
            if parser.has_section('humidifier'):
                self.humidifier = dict(parser.items('humidifier'))
            log.debug("Current INI Configuration read successfully.")
            
        if config_dict and type(config_dict) is dict:
            log.debug("Reading parameters from INI configuration dictionary.")
            
            if not validate_config_dict(config_dict):
                log.error("Given INI configuration dictionary is not valid.")
				#Failed validation should be handled properly... throw back flash message to user or similar.
            
            self.general['update_interval'] = self._get_str_from_dict(config_dict, 'general_update_interval')
#            self.general['switch_param'] = self._get_onoff_from_dict(config_dict, 'general_switch_param')
#            self.general['numerical_value'] = self._get_float_from_dict(config_dict, 'general_numerical_value')
            
#            self.specific['something'] = self._get_str_from_dict(config_dict, 'specific_something')
#            self.specific['enabled'] = self._get_bool_from_dict(config_dict, 'specific_enabled')
#            self.specific['number'] = self._get_float_from_dict(config_dict, 'specific_number')

            self.tempodb['enabled'] = self._get_bool_from_dict(config_dict, 'tempodb_enabled')
            self.tempodb['key'] = self._get_str_from_dict(config_dict, 'tempodb_key')
            self.tempodb['secret'] = self._get_str_from_dict(config_dict, 'tempodb_secret')
            
            self.plotly['enabled'] = self._get_bool_from_dict(config_dict, 'plotly_enabled')
            self.plotly['key'] = self._get_str_from_dict(config_dict, 'plotly_key')
            self.plotly['user'] = self._get_str_from_dict(config_dict, 'plotly_user')

            self.ds18b20_1['enabled'] = self._get_bool_from_dict(config_dict, 'ds18b20_1_enabled')
            self.ds18b20_1['name'] = self._get_str_from_dict(config_dict, 'ds18b20_1_name')
            self.ds18b20_1['path'] = self._get_str_from_dict(config_dict, 'ds18b20_1_path')

            self.ds18b20_2['enabled'] = self._get_bool_from_dict(config_dict, 'ds18b20_2_enabled')
            self.ds18b20_2['name'] = self._get_str_from_dict(config_dict, 'ds18b20_2_name')
            self.ds18b20_2['path'] = self._get_str_from_dict(config_dict, 'ds18b20_2_path')

            self.wunderground['enabled'] = self._get_bool_from_dict(config_dict, 'wunderground_enabled')
            self.wunderground['key'] = self._get_str_from_dict(config_dict, 'wunderground_key')
            self.wunderground['state'] = self._get_str_from_dict(config_dict, 'wunderground_state')
            self.wunderground['city'] = self._get_str_from_dict(config_dict, 'wunderground_city')
            self.wunderground['retry'] = self._get_str_from_dict(config_dict, 'wunderground_retry')

            self.nest['enabled'] = self._get_bool_from_dict(config_dict, 'nest_enabled')
            self.nest['login'] = self._get_str_from_dict(config_dict, 'nest_login')
            self.nest['password'] = self._get_str_from_dict(config_dict, 'nest_password')

            self.humidifier['enabled'] = self._get_bool_from_dict(config_dict, 'humidifier_enabled')
            self.humidifier['gpio_pin'] = self._get_str_from_dict(config_dict, 'humidifier_gpio_pin')
            self.humidifier['deadband'] = self._get_str_from_dict(config_dict, 'humidifier_deadband')
            self.humidifier['min_humidity'] = self._get_str_from_dict(config_dict, 'humidifier_min_humidity')
            self.humidifier['max_humidity'] = self._get_str_from_dict(config_dict, 'humidifier_max_humidity')
            
            log.debug("INI configuration dictionary read.")

    def to_dict(self):
        ''' Creates config_dict from object '''
        
        config_dict = dict()
        
        config_dict['general_update_interval'] =  self.general['update_interval']

        config_dict['tempodb_enabled'] =  self.tempodb['enabled']
        config_dict['tempodb_key'] =  self.tempodb['key']
        config_dict['tempodb_secret'] =  self.tempodb['secret']

        config_dict['plotly_enabled'] =  self.plotly['enabled']
        config_dict['plotly_key'] =  self.plotly['key']
        config_dict['plotly_user'] =  self.plotly['user']
        
        config_dict['ds18b20_1_enabled'] =  self.ds18b20_1['enabled']
        config_dict['ds18b20_1_name'] =  self.ds18b20_1['name']
        config_dict['ds18b20_1_path'] =  self.ds18b20_1['path']
        
        config_dict['ds18b20_2_enabled'] =  self.ds18b20_2['enabled']
        config_dict['ds18b20_2_name'] =  self.ds18b20_2['name']
        config_dict['ds18b20_2_path'] =  self.ds18b20_2['path']

        config_dict['wunderground_enabled'] =  self.wunderground['enabled']
        config_dict['wunderground_key'] =  self.wunderground['key']
        config_dict['wunderground_state'] =  self.wunderground['state']
        config_dict['wunderground_city'] =  self.wunderground['city']
        config_dict['wunderground_retry'] =  self.wunderground['retry']

        config_dict['nest_enabled'] =  self.nest['enabled']
        config_dict['nest_login'] =  self.nest['login']
        config_dict['nest_password'] =  self.nest['password']

        config_dict['humidifier_enabled'] =  self.humidifier['enabled']
        config_dict['humidifier_gpio_pin'] =  self.humidifier['gpio_pin']
        config_dict['humidifier_deadband'] =  self.humidifier['deadband']
        config_dict['humidifier_min_humidity'] =  self.humidifier['min_humidity']
        config_dict['humidifier_max_humidity'] =  self.humidifier['max_humidity']
        
        return config_dict

    def updateConfigFile(self):
        '''Updated actuall INI configuration file'''
        
        parser = SafeConfigParser()
        
        for section in ['general', 'tempodb', 'plotly', 'ds18b20_1', 'ds18b20_2', 'wunderground', 'nest', 'humidifier']:
            section_dict = getattr(self, section)
            parser.add_section(section)
            for section_key in section_dict.keys():
                parser.set(section, section_key, str(section_dict[section_key]))

        parser.write(sys.stdout)

        config_file = open(self.config_filepath, 'w')
        parser.write(config_file)
        config_file.close()
        
    def _get_bool_from_dict(self, config_dict, key_name):
        if key_name in config_dict:
            result = bool(config_dict[key_name])
        else:
            result = False
        return result
    
    def _get_str_from_dict(self, config_dict, key_name):
        if key_name in config_dict:
            result = str(config_dict[key_name])
        else:
            result = ''
        return result
        
    def _get_onoff_from_dict(self, config_dict, key_name):
        if key_name in config_dict:
            result = str(config_dict[key_name])
        else:
            result = ''            
        if result != 'on':
            result = 'off'
        return result
        
    def _get_int_from_dict(self, config_dict, key_name):
        try:
            if key_name in config_dict:
                result = int(config_dict[key_name])
            else:
                result = 0
        except:
            result = 0
        return result
    
    def _get_float_from_dict(self, config_dict, key_name):
        try:
            if key_name in config_dict:
                result = float(config_dict[key_name])
            else:
                result = 0
        except:
            result = 0
        return result

def purge_config_dict(post_dict):
    ''' Removes all unnecessary keys from given dict '''
    allowed_keys = ['general_update_interval', 'tempodb_enabled', 'tempodb_key', 'tempodb_secret', 'plotly_enabled', 'plotly_key', 'plotly_user', 'ds18b20_1_enabled', 'ds18b20_1_path', 'ds18b20_1_name', 'ds18b20_2_enabled', 'ds18b20_2_name', 'ds18b20_2_path', 'wunderground_enabled', 'wunderground_key', 'wunderground_state', 'wunderground_city', 'wunderground_retry', 'nest_enabled', 'nest_login', 'nest_password', 'humidifier_enabled', 'humidifier_gpio_pin', 'humidifier_deadband', 'humidifier_min_humidity', 'humidifier_max_humidity']
    result_dict = dict()
    
    for key in post_dict.keys():
        if key in allowed_keys:
            result_dict[key] = post_dict[key]
    return result_dict

def validate_config_dict(config_dict):
    return True
        
    
    
    
