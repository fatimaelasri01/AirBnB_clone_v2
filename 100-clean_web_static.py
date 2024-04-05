#!/usr/bin/python3
"""cleans old files"""

from fabric.api import *
import os
from datetime import datetime
import tarfile


env.hosts = ["3.85.177.61", "3.84.238.73"]
env.user = "ubuntu"

def do_clean(number=0):
    """removes all but given num of archives"""
    number = int(number)
    if number < 2:
        number = 1
    number += 1
    number = str(number)
    with lcd("versions"):
        local("ls -1t | grep web_static_.*\.tgz | tail -n +" +
              number + " | xargs -I {} rm -- {}")
    with cd("/data/web_static/releases"):
        run("ls -1t | grep web_static_ | tail -n +" +
            number + " | xargs -I {} rm -rf -- {}")
