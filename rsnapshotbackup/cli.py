# -*- coding: utf-8 -*-
# (c) 2012 Niko Böckerman <niko.bockerman@gmail.com>
# Released under the terms of the 2-clause BSD license.


SETTINGS_FOLDER = "/etc/rsnapshot-backup"
EMAIL_SETTINGS_FILE_NAME = "emailsettings.cfg"

SETTINGS_FILENAME = "settings.cfg"
RSNAPSHOTCONF_FILENAME = "rsnapshot.conf"

import argparse
import os
import psutil

from . import argumentparser
from . import settings
from . import emailing
from . import mounting
from . import rsnapshot


def changeDir():
    filePath = os.path.dirname(os.path.abspath(__file__))
    os.chdir(filePath)

def lowerResourceUsage():
    os.nice(20)
    p = psutil.Process(os.getpid())
    p.set_ionice(psutil.IOPRIO_CLASS_IDLE)

def main(argv):
    changeDir()
    lowerResourceUsage()

    emailsettingspath = os.path.join(SETTINGS_FOLDER, EMAIL_SETTINGS_FILE_NAME)
    emailsettings = settings.EmailSettings(emailsettingspath)
    try:
        emailsettings.load()
    except settings.SettingsError as e:
        print("Failed to read settings file:")
        print(e)
        return 1
    
    emailer = emailing.Emailing(emailsettings.fromAddr, emailsettings.toAddr, emailsettings.host, emailsettings.useSsl, emailsettings.username, emailsettings.password)
    
    parser = argumentparser.ArgParser(description="Backup wrapper tool for rsnapshot")
    parser.add_argument('backupConfig')
    parser.add_argument('retain')
    #parser.print_help()
    args = None
    try:
        args = parser.parse_args(argv[1:])
    except argparse.ArgumentError as e:
        subject = "Invalid call to launch rsnapshot-backup"
        message = ("Error message: " + e.message + "\n" +
                   "Received call: " + ' '.join(sys.argv))
        emailer.sendmail(subject, message)
        return 2

    backuppath = os.path.join(SETTINGS_FOLDER, args.backupConfig)
    backupsettingspath = os.path.join(backuppath, SETTINGS_FILENAME)
    backupsettings = settings.BackupSettings(backupsettingspath)
    try:
        backupsettings.load()
    except settings.SettingsError as e:
        subject = "Failed to read backup config file"
        message = "Error message: " + str(e)
        emailer.sendmail(subject, message)
        return 3
    
    mountpoint = None
    if backupsettings.mount:
        mountpoint = mounting.Mountpoint(backupsettings.mountpoint)
        try:
            mountpoint.mount()
        except mounting.MountError as e:
            subject = "Failed to mount requested filesystem"
            message = ("Error message:\n" + str(e))
            emailer.sendmail(subject, message)
            return 4
    
    #Launch backup
    rsnapshotconfpath = os.path.join(backuppath, RSNAPSHOTCONF_FILENAME)
    backup = rsnapshot.Rsnapshot(rsnapshotconfpath, args.retain)
    success, output = backup.backup()
    exitcode = 0
    if not success:
        subject = "Backup creation failed"
        emailer.sendmail(subject, output)
        exitcode = 5
    
    # Umount file system
    if mountpoint is not None:
        try:
            mountpoint.umount()
        except mounting.MountError as e:
            subject = "Failed to unmount requested filesystem after backup"
            message = ("Error message:\n" + str(e))
            emailer.sendmail(subject, message)
            if exitcode == 0:
                exitcode = 6

    return exitcode
    
