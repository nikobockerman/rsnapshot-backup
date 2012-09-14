# -*- coding: utf-8 -*-
# (c) 2012 Niko Böckerman <niko.bockerman@gmail.com>
# Released under the terms of the 2-clause BSD license.


import os
import subprocess

class MountError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def calledProcessError_to_str(error):
    return ("Called command: " + repr(error.cmd) + os.linesep +
            "Return code: " + str(error.returncode) + '\n' +
            "Output:\n" + error.output)

class Mountpoint():
    def __init__(self, mountpoint):
        self.mountpoint = mountpoint
        self.mounted = False
    
    def mount(self):
        # Check if mount point is valid
        if self.mountpoint is None:
            return
        # Check if mount point is already mounted
        if os.path.ismount(self.mountpoint):
            return
        # Try to mount
        try:
            subprocess.check_output(["mount", self.mountpoint], 
                                    stderr=subprocess.STDOUT, 
                                    universal_newlines=True)
            self.mounted = True
        except subprocess.CalledProcessError as e:
            raise MountError("Failed to mount " + self.mountpoint + ".\n" + 
                             calledProcessError_to_str(e))
        
    def umount(self):
        if not self.mounted:
            return
        # Try to unmount
        try:
            subprocess.check_output(["umount", self.mountpoint], 
                                    stderr=subprocess.STDOUT, 
                                    universal_newlines=True)
            self.mounted = False
        except subprocess.CalledProcessError as e:
            raise MountError("Failed to umount " + self.mountpoint + ".\n" + 
                             calledProcessError_to_str(e))
    

if __name__ == "__main__":
    '''
    Before testing, check that /etc/fstab has an entry pointing to
    /mnt/test,which can actually be mounted
    '''
    import sys
    import time
    
    mountpoint_path = "/mnt/test"
    print("Trying to mount " + mountpoint_path)
    mountpoint = Mountpoint(mountpoint_path)
    try:
        mountpoint.mount()
    except MountError as e:
        print(e)
        sys.exit(1)
    print("Mount was successful. Printing system mount points and waiting 2 seconds.")
    subprocess.call(["mount"])
    time.sleep(2)
    
    print ("Trying to umount " + mountpoint_path)
    try:
        mountpoint.umount()
    except MountError as e:
        print(e)
        sys.exit(1)
    print("Umount was successful. Printing system mount points.")
    subprocess.call(["mount"])
