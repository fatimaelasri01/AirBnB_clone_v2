#!/usr/bin/python3
"""fabfile to create a .tgz archive"""

import tarfile
from datetime import datetime
import os


def do_pack():
    """creates a .tgz archive containing contents of web_static dir"""

    #get the current date and time
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    #define the filename for the archive
    filename = "versions/web_static_{}.tgz".format(date)

    #create the versions dir if it doesn't exist
    if not os.path.exists("versions/"):
        os.mkdir("versions/")

    #create the .tgz archive
    with tarfile.open(filename, "w:gz") as tar:
        tar.add("web_static", arcname=os.path.basename("web_static"))

    #return the path to the archive if it was created successfully
    if os.path.exists(filename):
        return filename
    else:
        return None
