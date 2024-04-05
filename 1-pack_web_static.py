#!/usr/bin/python3
"""fabfile to create a .tgz archive"""

import tarfile
from datetime import datetime
import os


def do_pack():
    """creates a .tgz archive containing contents of web_static dir"""

    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)

    if not os.path.exists("versions/"):
        os.mkdir("versions/")

    with tarfile.open(filename, "w:gz") as tar:
        tar.add("web_static", arcname=os.path.basename("web_static"))

    if os.path.exists(filename):
        return filename
    else:
        return None
