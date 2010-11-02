from base import BaseProcessor
from ..lib.xml2dict import xml2dict
import sys

__all__ = ['MongoSaver',]

class MongoSaver(BaseProcessor):
    """
    Convert XML to dict, clean dict, then put that dict into a mongo document and save it.
    
    If you define your mongo model like this, then this saver will work with it, but you'll probably find it hard to query:
    
    class TitleWork(Document):
        _attributes = DictField()
        key1 = ListField(DictField())
        key2 = ListField(DictField())
        key3 = ListField(DictField())
        ...
        
    where key1..n are the dictionary keys corresponding to child tags of the element you're saving.
    
    """
    def __init__(self, model):
        self.model = model
        
    def clean(self, d):
        return d
    
    def __call__(self, tag):
        d = xml2dict(tag)
        d = self.clean(d)
        
        m, created = self.model.objects.get_or_create(**d)