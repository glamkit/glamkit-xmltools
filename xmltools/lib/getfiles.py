import os
import re

def getfiles(path, regex=r"", recursive=True, followlinks=True):
    """generates a list of file paths of files in given folder that match a given regex"""
    
    rex = re.compile(regex)

    if os.path.isfile(path):
        p = os.path.abspath(path)
        if rex.search(p):
            yield p
    else: 
        if recursive:    
            for root, dirs, files in os.walk(path, followlinks):
                for f in files:
                    p = os.path.abspath(os.path.join(root, f))
                    if rex.search(p):
                        yield p
        else:
            for f in os.listdir(path):
                p = os.path.abspath(os.path.join(path, f))
                if os.path.isfile(p):
                    if rex.search(p):
                        yield p