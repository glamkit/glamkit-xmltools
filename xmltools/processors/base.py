import sys

__all__ = ['BaseProcessor', 'DebugProcessor']

class BaseProcessor(object):    
    def __call__(self, tag):
        raise NotImplemented("Subclasses of BaseSaver need to implement __call__().")

class DebugProcessor(BaseProcessor):
    def __init__(self, *args, **kwargs):
        pass
        
    def __call__(self, tag):
        sys.stderr.write("Fake saving %s\n" % (tag, ))
