from base import BaseProcessor
from ..lib.xml2dict import xml2dict
import sys
__all__ = ['MongoSaver',]


DEBUG_ON_IMPORT_SAVE_ERROR = True

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
        u = xml2dict(tag)
        d = self.clean(u)
        
        try:
        
            if d is not None:
                try:
                    m = self.model.objects.get(id=d['id'])
                    for k, v in d.iteritems():
                        setattr(m, k, v)
                        m.save()
                except self.model.DoesNotExist:
                    m = self.model.objects.create(**d)
                    m.save()
        except Exception as e:
            if DEBUG_ON_IMPORT_SAVE_ERROR:
                from pprint import pprint
                print e
                import pdb; pdb.set_trace()
            else:
                raise e