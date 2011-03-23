# -*- coding: utf-8 -*-

# A file-like object that cleans up each line, if necessary.
# This is useful if your xml file declares utf-8 and yet there are iso values in the actual file
# http://stackoverflow.com/questions/2352840/parsing-broken-xml-with-lxml-etree-iterparse

class File(object):
    def __init__(self, filename):
        self.f = open(filename, 'rt')

    def read(self, size=None):
        return self.f.next() #.replace('\x1e', '').replace('some other bad character...' ,'')
        