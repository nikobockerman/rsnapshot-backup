# -*- coding: utf-8 -*-
# (c) 2012 Niko Böckerman <niko.bockerman@gmail.com>
# Released under the terms of the 2-clause BSD license.


BACKUPSSETTINGS_SECTION = "BackupSettings"
MOUNTPOINT_OPTION = "Mountpoint"  # Optional
CONFIG_OPTION = "ConfigFile"

EMAIL_SECTION="EmailSettings"
SMTP_HOST_OPTION="Host"
SMTP_SSL_OPTION="UseSSL"
SMTP_USER_OPTION="Username"  # Optional, but if set also password needs to be set
SMTP_PASSWD_OPTION="Password"  # Optional, but if set also username needs to be set
EMAIL_FROM_OPTION="FromAddr"
EMAIL_TO_OPTION="ToAddr"

import configparser
import os

class SettingsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Settings():
    def __init__(self, settingsPath):
        self.settingsPath = settingsPath
    
    def load(self):
        if not os.access(self.settingsPath, os.F_OK):
            raise SettingsError("Settings file (" + self.settingsPath + ") does not exists")
        if not os.access(self.settingsPath, os.R_OK):
            raise SettingsError("Permissions denied for reading settings file (" + self.settingsPath + ")")
        config = configparser.ConfigParser()
        try:
            with open(self.settingsPath, 'r') as configfile:
                config.read_file(configfile)
        except IOError as error:
            if error.errno == 2:
                raise SettingsError("Config file (" + self.settingsPath + ") does not exists!")
            else:
                raise SettingsError("Following error occurred while reading config file!" + str(error))
        except (configparser.DuplicateSectionError, configparser.DuplicateOptionError, configparser.MissingSectionHeaderError) as e:
            raise SettingsError("Config file is invalid: " + e)
        return config


class EmailSettings(Settings):
    def __init__(self, settings_path):
        super(EmailSettings, self).__init__(settings_path)
        self.host = None
        self.useSsl = None
        self.fromAddr = None
        self.toAddr = None
        self.requireLogin = None
        self.username = None
        self.password = None
        
    def load(self):
        config = super(EmailSettings, self).load()
        try:
            config[EMAIL_SECTION]
        except KeyError as e:
            raise SettingsError("Settings file does not contain required section: " + repr(e))
        try:
            self.host = config[EMAIL_SECTION][SMTP_HOST_OPTION]
            if config[EMAIL_SECTION][SMTP_SSL_OPTION] in ["True",  "true"]:
                self.useSsl = True
            elif config[EMAIL_SECTION][SMTP_SSL_OPTION] in ["False",  "false"]:
                self.useSsl = False
            else:
                raise SettingsError("Invalid settings value [" + EMAIL_SECTION + "][" + SMTP_SSL_OPTION + "]. Expected 'True' or 'False'")
            self.fromAddr = config[EMAIL_SECTION][EMAIL_FROM_OPTION]
            self.toAddr = config[EMAIL_SECTION][EMAIL_TO_OPTION]
        except KeyError as e:
            raise SettingsError("Settings file does not contain required option: " + repr(e))
        
        self.requireLogin = False
        self.username = ""
        self.password = ""
        try:
            self.username = config[EMAIL_SECTION][SMTP_USER_OPTION]
            self.password = config[EMAIL_SECTION][SMTP_PASSWD_OPTION]
        except KeyError:
            pass

class BackupSettings(Settings):
    def __init__(self, settings_path):
        super(BackupSettings, self).__init__(settings_path)
        self.mount = None
        self.mountpoint = None
        self.configFile = None
    
    def load(self):
        config = super(BackupSettings, self).load()
        try:
            config[BACKUPSSETTINGS_SECTION]
        except KeyError as e:
            raise SettingsError("Settings file does not contain required section: " + repr(e))
        
        try:
            self.configFile = config[BACKUPSSETTINGS_SECTION][CONFIG_OPTION]
        except KeyError as e:
            raise SettingsError("Settings file does not contain required option: " + repr(e))
        
        self.mount = False
        self.mountpoint = None
        try:
            self.mountpoint = config[BACKUPSSETTINGS_SECTION][MOUNTPOINT_OPTION]
            self.mount = True
        except KeyError as e:
            pass


if __name__ == "__main__":
    import sys
    settings_path = "settings.cfg"
    print ("Reading settings file:", settings_path)

    try:
        settings = Settings(settings_path)
    except SettingsError as e:
        print ("Creating settings object failed:", e)
        sys.exit(1)

    print ("Mountpoint read from settings:", settings.mountpoint)
