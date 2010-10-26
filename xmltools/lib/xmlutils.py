
def findtext(elem, name):
    return elem.find(name).text

def pad_and_insert(L, index, item):
    """Make L[index] = item, padding list with Nones if necessary"""
    len_L = len(L)
    padding = 1 + index - len_L
    if padding > 0:
        L.extend([None] * padding)
    L[index] = item

def findalltext(elem, name):
    els = elem.findall(name)
    r = []
    for el in els:
        try:
            row = int(el.attrib['row']) - 1 # a bit vernon-specific, this.
            pad_and_insert(r, row, el.text)
        except KeyError:
            r.append(el.text)
    return r
