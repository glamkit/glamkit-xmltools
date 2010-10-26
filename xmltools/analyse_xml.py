#!/usr/bin/env python
# −*− coding: UTF−8 −*−
from optparse import OptionParser #, make_option, OptionError
import os
from lib.analyse import xmlanalyse
from lib.getfiles import getfiles
import sys

           
def main():
    usage = "usage: %prog [options]\n\nPrints a list of paths for all XML files found at the given paths."
            
    parser = OptionParser(usage=usage)

    parser.add_option("-p", "--path", action="store", dest="path", default=".", help="specify the folder to analyse")
    parser.add_option("-r", action="store_true", dest="recursive", default=False, help="traverse the given folder recursively")
    parser.add_option("-l", action="store_true", dest="list_only", default=False, help="only list the xml files that would be analysed")
    parser.add_option("-n", action="store", dest="sample_length", default=5, help="provide this many samples of each element's text")

    (options, args) = parser.parse_args()

    paths = getfiles(path=options.path, regex=r"\.xml$", recursive=options.recursive)

    if options.list_only:
        for p in paths:
            print p
        sys.exit(0)
    
    xmlanalyse(paths, sample_length = options.sample_length)
    
if __name__ == "__main__":
    main()