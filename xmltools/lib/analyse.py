from lxml import etree
from pprint import pprint
import sys
import csv
import re
csv_header=("path", "min_valency", "max_valency","sample_values", "attributes")


NS_RE = re.compile(r"\{.*?\}")
BREAK = -1

def _fast_iter(context, func, **params):
    n = params.pop('n', 0)
    for event, elem in context:
        status = func(elem, event, **params)
        if status == BREAK:
            break
        if event=="end":
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        n += 1
        if n % 10000 == 0:
            sys.stderr.write("processing %s elements...\n" % n)
    del context
    return n

def _remove_ns(tag):
    return re.sub(NS_RE, "", tag)

def _get_path(elem, separator="."):
    an = elem.iterancestors()
    anlist = [_remove_ns(e.tag) for e in an]
    anlist.reverse()
    anlist += [_remove_ns(elem.tag)]

    return separator.join(anlist)


def _get_children_from_analysis(path, analysis):
    keys = analysis.keys()
    for k in keys:
        if k.startswith(path) and k != path: # k is a decendent, but not necessarily a child.
            if len(k[len(path):].split('.')) == 2: #it's a child ['', 'child']
                yield k



def update_analysis(elem, event, analysis, sample_length):
    path = _get_path(elem)

    if event == "start":
        if not analysis.has_key(path):
            analysis[path] = {
                'valence_current': 0,
                'valence_min': sys.maxint,
                'valence_max': 0,
                'values': set(),
                'attributes': {},
            }
            
        analysis[path]['valence_current'] += 1
        #maintain max
        if analysis[path]['valence_current'] > analysis[path]['valence_max']:
            analysis[path]['valence_max'] = analysis[path]['valence_current']

        #attributes
        for attr in elem.keys():
            av = analysis[path]['attributes'].get(attr, set())
            if len(av) < sample_length:
                av.add(elem.get(attr))
                analysis[path]['attributes'][attr] = av


    if event=="end":
        # maintain min
        for c in _get_children_from_analysis(path, analysis):
            if analysis[c]['valence_current'] < analysis[c]['valence_min']:
                analysis[c]['valence_min'] = analysis[c]['valence_current']
            analysis[c]['valence_current'] = 0
        # sample values
        if len(analysis[path]['values']) < sample_length:
            try:
                v = elem.text.strip()
                if v:
                    analysis[path]['values'].add(v)
            except AttributeError:
                pass

def _attributestring(attrdict):
    ss = []
    for key, value in attrdict.iteritems():
        s = "%s = (\"%s\")" % (_remove_ns(key), "\", \"".join(value))
        ss.append(s)
    
    return "\r\n\r\n".join(ss)

def xmlanalyse(files, sample_length=5):
    """ returns a csv of xml paths and analysed values, showing, for example, how many records exist for every path in an xml file """

    analysis = {}
    
    n = 0
    
    for f in files:
        sys.stderr.write("processing %s\n" % f)
        context = etree.iterparse(f, events=('start', 'end'))
        n = _fast_iter(context, update_analysis, n = n, sample_length = sample_length, analysis=analysis)

    writer = csv.writer(sys.stdout)
    writer.writerow(csv_header)

    listanalysis = [x for x in analysis.iteritems()]
    listanalysis.sort()

    for key, value in listanalysis:
        v = []
        v.append(key) #path
        if value['valence_min'] == sys.maxint: #top-level nodes do this.
            value['valence_min'] = value['valence_max']
        v.append(value['valence_min'])
        v.append(value['valence_max'])
        v.append("\r\n\r\n".join(value['values']))
        v.append(_attributestring(value['attributes']))
        
        writer.writerow(v)