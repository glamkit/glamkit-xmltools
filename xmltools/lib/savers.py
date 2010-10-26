import xmlutils
from constants import *
import sys

class BaseSaver(object):
    def __init__(self, elem):
        self.elem = elem

    def warn(self, tag, category=""):
        sys.stderr.write("WARNING: %s %s isn't handled in %s.\n" % (category, tag, self.elem))

    def save(self, create_only):
        raise NotImplementedError("subclasses of BaseSaver need to implement 'save'")

class NullSaver(BaseSaver):
    
    def save(self, create_only):
        print "Not saving %s; freeing up memory." % self.elem.tag
        return DISCARD_AFTER

class StringHelperSaver(BaseSaver):
    
    SINGLETON_STRING_MAP = {}
    LIST_STRING_MAP = {}
    SPECIAL_FIELDS_MAP = {}
    IGNORE_FIELDS = []
    
    def get_values(self):
        values = {}
        tags = set()
        for child in self.elem.getchildren():
            tags.add(child.tag)
            
        for tag in tags:
            if self.SINGLETON_STRING_MAP.has_key(tag):
                values[self.SINGLETON_STRING_MAP[tag]] = xmlutils.findtext(self.elem, tag)
            elif self.LIST_STRING_MAP.has_key(tag):
                values[self.LIST_STRING_MAP[tag]] = xmlutils.findalltext(self.elem, tag)
            elif self.SPECIAL_FIELDS_MAP.has_key(tag):
                try:
                    handler_result = getattr(self, 'handle_%s' % tag)(self.elem.findall(tag), values)

                    valueskey = self.SPECIAL_FIELDS_MAP[tag]
                    if valueskey:
                        values[valueskey] = handler_result
                        
                except AttributeError as e: #Other attribute errors (within the function) sometimes throw this
                    self.warn(tag, category="Special field")
                    import pdb; pdb.set_trace()
            elif tag in self.IGNORE_FIELDS:
                pass
            else:
                self.warn(tag)

        return values
    
    def filter_nones_from_lists(self, values):
        for key in self.LIST_STRING_MAP.values(): #values is the RHS of the mapping
            if values.has_key(key):
                values[key] = filter(lambda x: x is not None, values[key])
    
    def clean(self, values):
        pass
    
    def save(self, create_only):
        # call get_values_dict
        raise NotImplementedError("subclasses of StringHelperSaver need to implement 'save'")        