from rdflib import Graph, RDF, OWL, RDFS
from rdflib.namespace import NamespaceManager

# Turtle-Datei laden
g = Graph()
g.parse("DigitalReference.ttl", format="turtle")

print(g)
# Dynamische Erkennung und Binden aller Namespaces
namespace_manager = NamespaceManager(g)
for prefix, namespace in g.namespaces():
    print(f"Erkannter Namespace: {prefix} -> {namespace}")
    namespace_manager.bind(prefix, namespace)

# Sicherstellen, dass alle Entitäten mit owl:Class korrekt definiert sind
for s, p, o in g.triples((None, RDF.type, None)):
    if o == OWL.Class:
        print(f"{s} ist korrekt als owl:Class definiert")
    elif o == RDFS.Class:
        print(f"{s} ist eine rdfs:Class. Wird zu owl:Class geändert.")
        g.remove((s, RDF.type, RDFS.Class))
        g.add((s, RDF.type, OWL.Class))
    else:
        print(f"{s} hat einen anderen Typ: {o}")

# Optional: Weitere Verarbeitung für andere Typen wie rdf:Property oder skos:Concept
# Beispiel für rdf:Property
for s, p, o in g.triples((None, RDF.type, RDF.Property)):
    print(f"{s} ist eine Eigenschaft (rdf:Property)")

# Serialisierung der Ausgabe in RDF/XML mit allen Namespaces
g.serialize("output1.rdf", format="pretty-xml")
print("Konvertierung abgeschlossen. Ausgabe gespeichert in 'output.rdf'")
