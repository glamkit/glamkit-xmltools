from lxml import etree
from lxml.cssselect import CSSSelector
from lib.constants import BREAK, DO_NOT_DISCARD
import sys
from lib.iterxml import multifile_iter_elems

def node(selector, kallable, **kwargs):
    return {
        'selector': selector,
        'callable': kallable,
        'kwargs': kwargs,
    }

class BaseHandler(object):
    """
    In subclasses, define nodes, mapping of CSS-style selectors to callables:
    
    nodes = (
        node('mavis > Organisation', org_callable, **kwargs),
        node('mavis > Person', person_callable, **kwargs),
        node('mavis > SeriesWork', work_callable, **kwargs),
        node('mavis > TitleWork', title_work_callable, **kwargs),
    )
    
    Only the value of the final matching callable is returned to the parent.
    
    Then call .harvest(paths). Every time a selector is matched, the elem, and kwargs, will be passed to the corresponding callable.
    
    Each callable should:
    
        1) handle the contents of XML elem.
        2) Log for itself that the handle has happened (e.g. for post-batch-handle cleaning, etc).
        3) Return constants.DO_NOT_DISCARD if the memory taken by this elem is NOT to be freed up after the callable is called - ie another handler should run.
    """
    
    def _make_handler_list(self):
        self.HANDLERS = []
        for node in self.handle_nodes:
            #CSSSelector() compiles into XPath
            namespaces = getattr(self, 'namespaces', None)
            self.HANDLERS.append((CSSSelector(node['selector'], namespaces=namespaces), node['callable'], node['kwargs']))
    
    def __init__(self, *args, **kwargs):
        self._make_handler_list()

    def handle_elem(self, elem):
        root = elem.getroottree().getroot()
        #Do the cleaning
        x = DO_NOT_DISCARD
        for selector, kallable, kwargs in self.HANDLERS:
            # get the elems that match this selector (as loaded into the root so far)
            if elem in selector(root):
                x = kallable(elem, **kwargs)
                if x is not None and x & BREAK:
                    break
        return x         
    
    def process(self, files):
        multifile_iter_elems(files, callable_start=None, callable_end=self.handle_elem)
        self.post_harvest()
        
    def post_harvest(self):
        pass