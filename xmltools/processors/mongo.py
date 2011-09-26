from base import BaseProcessor
__all__ = ['MongoSaver',]

"""
NOTE! The way this works has significantly diverged from .django.DjangoSaver, and should probably be brought into line.
"""

class MongoSaver(BaseProcessor):
    """
    Convert XML to dict, clean dict, then put that dict into a mongo document instance and save it.
    
    You'll want to override 'clean', and return the kwargs for the document instance creation.

    We force the use of 'id' for PK.
    """
    def __init__(self, model):
        self.model = model
        self.count = 0
        self.fails = 0
        
    def make_kwargs(self, tag):
        raise NotImplemented("Define a `make_kwargs` method that takes an XML tag, and returns a kwargs dictionary which can be passed to a model's `create()` call.")

    def __call__(self, tag):
        kwargs = self.make_kwargs(tag)

        if kwargs is not None:
            m = self.model.objects.create(**kwargs)
            self.count += 1
            if self.count % 100 == 0:
                print "saved %s items" % self.count
        else: #d is none (fail)
            self.fails += 1
            if self.fails % 10 == 0:
                print "SKIPPED %s items" % self.fails