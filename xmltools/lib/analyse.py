from pprint import pprint
import sys
import csv
csv_header=("path", "min_valency", "max_valency","sample_values", "attributes")
from iterxml import multifile_iter_elems
from utils import remove_ns, get_path

def _get_children_from_analysis(path, analysis):
    keys = analysis.keys()
    for k in keys:
        if k.startswith(path) and k != path: # k is a decendent, but not necessarily a child.
            if len(k[len(path):].split('.')) == 2: #it's a child ['', 'child']
                yield k


def analyse_start(elem, analysis, sample_length):
    path = get_path(elem)

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


def analyse_end(elem, analysis, sample_length):
    path = get_path(elem)

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
        s = "%s = (\"%s\")" % (remove_ns(key), "\", \"".join(value))
        ss.append(s)
    
    return "\r\n\r\n".join(ss)

def xmlanalyse(files, sample_length=5):
    """ returns a csv of xml paths and analysed values, showing, for example, how many records exist for every path in an xml file """

    analysis = {}
    
    multifile_iter_elems(files, analyse_start, analyse_end, sample_length = sample_length, analysis=analysis)
    
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