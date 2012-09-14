# -*- coding: utf-8 -*-
# (c) 2012 Niko Böckerman <niko.bockerman@gmail.com>
# Released under the terms of the 2-clause BSD license.


import subprocess

RSNAPSHOT = "rsnapshot"
RSNAPSHOT_SHORT_ARGS = "-v"

class Rsnapshot:
    def __init__(self, config_file, retain):
        self.config_file = config_file
        self.retain = retain
    
    def backup(self):
        """
        Executes rsnapshot.
        Returns a tuple containing a boolean and output.
        If error occurred during backup creation, boolean is False and otherwise it is True.
        If boolean is False, then the output contains the output of the rsnapshot run
        """
        cmd = [RSNAPSHOT, RSNAPSHOT_SHORT_ARGS, "-c", self.config_file, self.retain]
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            output = output.decode("utf-8")
            return (True, output)
        except subprocess.CalledProcessError as e:
            return (False, e.output.decode("utf-8"))


if __name__ == "__main__":
    rsnapshot = Rsnapshot("conffile.conf", "hourly")
    success, output = rsnapshot.backup()
    print ("Result was: " + str(success))
    print ("Output was:\n" + output)
    
