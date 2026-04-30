from owlready2 import get_ontology

# Load the dictionary from random_classes.py
from randomClasses import random_words_map

# Load the ontology
onto = get_ontology("DigitalReference.rdf").load()

# Get all classes from the ontology
classes = list(onto.classes())
ontology_iris = {cls.iri for cls in classes}

# Check each IRI in the dictionary
missing_iris = []
found_iris = []

for key, iri in random_words_map.items():
    if iri in ontology_iris:
        found_iris.append((key, iri))
    else:
        missing_iris.append((key, iri))

# Print results
print(f"Total IRIs in dict: {len(random_words_map)}")
print(f"Found in RDF: {len(found_iris)}")
print(f"Missing from RDF: {len(missing_iris)}")
print(missing_iris)

if missing_iris:
    print("\nMissing IRIs:")
    for key, iri in missing_iris:
        print(f"  Key {key}: {iri}")
else:
    print("\n✓ All IRIs found in the RDF file!")