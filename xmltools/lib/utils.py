import re

NS_RE = re.compile(r"\{.*?\}")

def remove_ns(tag):
    return re.sub(NS_RE, "", tag)

def get_path(elem, separator="."):
    an = elem.iterancestors()
    anlist = [remove_ns(e.tag) for e in an]
    anlist.reverse()
    anlist += [remove_ns(elem.tag)]

    return separator.join(anlist)

camelcase_to_underscore = lambda str: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str).lower().strip('_')