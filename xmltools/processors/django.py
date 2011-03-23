from base import BaseProcessor
from ..lib.xml2dict import xml2dict
import sys
__all__ = ['DjangoSaver',]


DEBUG_ON_IMPORT_SAVE_ERROR = True

class DjangoSaver(BaseProcessor):
    """
    Convert XML to dict, clean dict, then put that dict into a django model instance and save it.
 
    You'll want to override 'clean', and return the kwargs for the model instance creation.

    We force the use of 'id' for PK.
        
    """
    def __init__(self, model):
        self.model = model
        self.count = 0
        self.fails = 0
        
    def clean(self, attribs):
        return attribs
    
    def __call__(self, tag):
        u = xml2dict(tag)
        d = self.clean(u)
                
        try:
            if d is not None:
                try: #update (deleting from a RDBMS updates FK)
                    m = self.model.objects.get(pk=d['id'])
                    del d['id']
                    for k,v in d.items():
                        setattr(m, k, v)
                    m.save()             
                except self.model.DoesNotExist:
                    m = self.model(**d)
                    m.save()
                self.count += 1
                if self.count % 100 == 0:
                    print "saved %s items" % self.count
            else: #d is none (fail)
                self.fails += 1
                if self.fails % 10 == 0:
                    print "SKIPPED %s items" % self.fails
        
        except Exception as e:
            if DEBUG_ON_IMPORT_SAVE_ERROR:
                from pprint import pprint
                pprint(e)
                pprint(u)
                pprint(d)
                import pdb; pdb.set_trace()
            else:
                raise e