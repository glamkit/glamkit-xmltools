from utils import remove_ns, camelcase_to_underscore

def xml2dict(tag):
    r = {}
    
    #value
    if tag.text is not None:
        v = tag.text.strip()
        if v:
            r['_value'] = v 
    
    #attributes
    if tag.keys():
        r['_attributes'] = {}
    for k in tag.keys():
        _k = remove_ns(k)
        _k = camelcase_to_underscore(_k)
        r['_attributes'][_k] = tag.get(k)
        
    for child in tag.getchildren():
        ctag = remove_ns(child.tag)
        ctag = camelcase_to_underscore(ctag)
        #assuming every child is potentially a list
        l = r.get(ctag, [])
        l.append(xml2dict(child))
        r[ctag] = l
    return r