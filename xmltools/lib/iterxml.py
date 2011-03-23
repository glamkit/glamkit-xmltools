"""
A pattern for iterating through a list of XML files, calling a callable at the start and end of each elem, and freeing up the memory used by that elem endwards.

If callable returns constants.DO_NOT_DISCARD, then the memory is NOT freed up.

Usage:

    iter_elems(path_to_xml, callable_start, callable_end, start_args, start_kwargs, end_args, end_kwargs)

or, for several XML files:

    multifile_iter_elems(paths_to_xmls, callable_start, callable_end, start_args, start_kwargs, end_args, end_kwargs)

"""
from lxml import etree
from constants import BREAK, DISCARD_AFTER
import sys
from files import File

def _fast_iter(context, callable_start, callable_end, *args, **kwargs):
    _iter_count = kwargs.pop('_iter_count', 0)
    for event, elem in context:
        if event=="start":
            status = callable_start(elem, *args, **kwargs)
        elif event=="end":
            status = callable_end(elem, *args, **kwargs)       
        if status is not None and status & BREAK:
            break
        if event=="end":
            if status is None or status & DISCARD_AFTER:
                elem.clear()
                while elem.getprevious() is not None: #delete parent if I am the last item.
                    del elem.getparent()[0]
        _iter_count += 1
        if _iter_count % 10000 == 0:
            sys.stderr.write("processing %s elements...\n" % _iter_count)
    del context
    return _iter_count


def iter_elems(path_to_xml, callable_start, callable_end, encoding=None, file_model=File, *args, **kwargs):
    kwargs['_iter_count'] = kwargs.get('_iter_count', 0)
    sys.stderr.write("processing %s\n" % path_to_xml)
    events = []
    if callable_start is not None:
        events.append('start')
    if callable_end is not None:
        events.append('end')
    context = etree.iterparse(file_model(path_to_xml), events=events, encoding=encoding)
    return _fast_iter(context, callable_start, callable_end, *args, **kwargs)

def multifile_iter_elems(paths_to_xmls, callable_start, callable_end, encoding=None, file_model=File, *args, **kwargs):
    _iter_count = 0
    for path in paths_to_xmls:
        kwargs['_iter_count'] = _iter_count
        _iter_count = iter_elems(path, callable_start, callable_end, encoding, file_model=file_model, *args, **kwargs)