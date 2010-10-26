# from analyse import xmlanalyse, xmlsample
# from lxml import etree
# from lxml.cssselect import CSSSelector
# from constants import *
# import sys
# 
# class BaseHarvester(object):
#     
#     SAVE_THESE = []
#     CLEAN_THESE = []    
#     
#     def __init__(self, filename):
#         self.filename = filename
#         self.SAVE_THESE_SELECTORS = self._make_selector_list(self.SAVE_THESE)
#         self.CLEAN_THESE_SELECTORS = self._make_selector_list(self.CLEAN_THESE)
#                 
#     @staticmethod
#     def _make_selector_list(inlist):
#         r = []
#         for selector, fns in inlist:
#             if not hasattr(fns, "__iter__"):
#                 fns = [fns]
#             r.append((CSSSelector(selector), fns))
#         return r
#     
#     def fast_iter(self, context, endfunc):
#         n = 0
#         """A function to loop through a context, calling func each time, and then clean up unneeded references"""
#         for event, elem in context:
#             if event=="start":
#                 startfunc(elem)
#             elif event=="end":
#                 status = endfunc(elem)
#                 if not status:
#                     status = DO_NOTHING
#                     
#                 #print status message
#                 if status & WAS_SAVED:
#                     n += 1
#                     if n % 100 == 0:
#                         print "Harvested %s items (most recent: %s)" % (n, elem.tag)
#                 #if we no longer need this element, remove it
#                 if status & DISCARD_AFTER:  
#                     elem.clear()
#                 
#                 #if we have saved it and no longer need it, we don't need its parent either, so we can delete all preceding siblings
#                 if status & DISCARD_AFTER and status & WAS_SAVED:
#                     while elem.getprevious() is not None:
#                         del elem.getparent()[0]
#                     
#         del context
#                 
#     def _handle_end(self, elem):
#         
#         root = elem.getroottree().getroot()
#         
#         #Do the cleaning
#         for selector, cleanfuncs in self.CLEAN_THESE_SELECTORS:
#             if elem in selector(root):
#                 for f in cleanfuncs:
#                     f(elem)
#         #Do the saving
#         for selector, saveclasses in self.SAVE_THESE_SELECTORS:
#             if elem in selector(root):
#                 for C in saveclasses[:-1]:
#                     C(elem).save(self.create_only)
#                 #The last function in the list gets to decide whether the data is kept or not
#                 status = saveclasses[-1](elem).save(self.create_only)
#                 if status is None:
#                     sys.stderr.write(
#                         "Warning: %s does not return a status. Consider returning DISCARD_AFTER to reduce memory footprint, or DO_NOTHING to remove this warning.\n" % (saveclasses[-1](elem).save)
#                     )
#                     status = DO_NOTHING
#                 return status | WAS_SAVED
#                 
#     def post_harvest(self):
#         pass
#                 
#     def harvest(self, ingest_only=False, create_only=False, post_harvest_only=False):
#         if not post_harvest_only:
#             self.pre_harvest()
# 
#             self.create_only = create_only
#             context = etree.iterparse(self.filename, events=('end',))
#             self.fast_iter(context, self._handle_end)
#         
#         if not ingest_only:
#             self.post_harvest()
#         
#     def analyse(self):
#         return xmlanalyse(self.filename)
#         
#     def sample(self, path, count=100):
#         return xmlsample(self.filename, path, count=100)