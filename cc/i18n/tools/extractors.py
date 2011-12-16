import re

from rdflib.Graph import Graph

TRANSLATION_BIT_RE = re.compile('\$\{([^\}]+)\}')

def extract_translations_from_rdf(fileobj, *args, **kwargs):
    filename = fileobj.name
    graph = Graph()
    graph.load(filename)

    matches = []
    for subject, predicate, obj in graph.triples((
            None, None, None)):
        if hasattr(obj, 'language') and obj.language == 'i18n':
            matches.extend(
                [(0, None, msg, "")
                 for msg in TRANSLATION_BIT_RE.findall(str(obj))])

    return matches
