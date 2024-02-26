import os
# from helper import *
import configparser
import inc.helper


class YPD_Config:
    file = './config.ini'
    config = None
    current = {}
    default = {'MAIN': {'downloads_dir': '.', 'theme': '1', 'dark_theme': 'Yes', 'type': 'Video', 'resolution': '720'}}

    # ----------------------------------------------------------------------------
    def __init__(self):
        # Create config file for first run
        if not os.path.isfile(self.file):
            try:
                f = open(self.file, "a")
                f.write('[MAIN]\n')
                f.write('downloads_dir = .\n')
                f.write('type = video\n')
                f.write('override = False\n')
                f.write('resolution = 720\n')
                f.write('dark_theme = Yes\n')
                f.write('theme = 1\n')
                f.write('override = False\n')
                f.close()
            except Exception as e:
                helper.show_error(e)
                raise Exception("Couldn't create config file!")
        
        self.read()
    # ----------------------------------------------------------------------------
    def save(self, section, key, value):
        try:
            self.config.set(section=section, option=key, value=value)
            self.config.write(open(self.file, 'w'))
        except Exception:
            raise Exception("Couldn't save settings")
    # ----------------------------------------------------------------------------
    def save_data(self, section, data):
        try:
            for (k, v) in data:
                self.config.set(section=section, option=k, value=v)
                self.current[section][k] = v

            self.config.write(open(self.file, 'w'))

        except Exception as e:
            helper.show_error(e)
            raise Exception("Couldn't save settings")
    # ----------------------------------------------------------------------------
    def get(self, section, key):
        # refresh config data
        self.config.read(self.file)
        
        if section in self.config:
            if key in self.config[section]:
                return self.config[section][key]
            else:
                print("{key} is not exists!")
                return ""
                # return self.default[section]

            # raise Exception("{key} is not exists!")
    # ----------------------------------------------------------------------------
    def get_section(self, section):
        return self.config[section]
    # ----------------------------------------------------------------------------
    def read(self):
        self.config = configparser.RawConfigParser()
        self.config.read(self.file)
    # ----------------------------------------------------------------------------
        