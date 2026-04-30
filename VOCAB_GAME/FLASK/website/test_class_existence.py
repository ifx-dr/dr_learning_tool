from owlready2 import get_ontology
import re


"""used to check the dictionary of classes to find out which cannot be found in the current DR file, also can be used to replace string ebginnings in case of base namespace change"""

# Load the dictionary from random_classes.py
from randomClasses import random_words_map

#replace here namespace prefixes that have changed
replacements = {
    "http://www.w3id.org/ecsel-dr-SCP#": "http://www.w3id.org/ecsel-dr-Planning-SCP#",
    "http://www.w3id.org/ecsel-dr-AH#": "http://www.w3id.org/ecsel-dr-Cloud-AH#",
    "http://www.w3id.org/ecsel-dr-ORG#": "http://www.w3id.org/ecsel-dr-Organization-ORG#",
    "http://www.w3id.org/ecsel-dr-PWR#": "http://www.w3id.org/ecsel-dr-Power-PWR#"
}

# Load the ontology
onto = get_ontology("static/ontologies/DigitalReference.rdf").load()

# Get all classes from the ontology
classes = list(onto.classes())
ontology_iris = {cls.iri for cls in classes}



def replace_iri_prefix(iri, replacements):
    """Replace IRI prefix if it matches any replacement rule"""
    for old_prefix, new_prefix in replacements.items():
        if iri.startswith(old_prefix):
            return iri.replace(old_prefix, new_prefix, 1)
    return iri

# Check each IRI in the dictionary
missing_iris = []
found_iris = []
replaced_iris = []
updated_dict = {}

for key, iri in random_words_map.items():
    if iri in ontology_iris:
        found_iris.append((key, iri))
        updated_dict[key] = iri
    else:
        # Try with replaced prefix
        replaced_iri = replace_iri_prefix(iri, replacements)
        if replaced_iri != iri and replaced_iri in ontology_iris:
            replaced_iris.append((key, iri, replaced_iri))
            found_iris.append((key, replaced_iri))
            updated_dict[key] = replaced_iri
        else:
            missing_iris.append((key, iri))
            updated_dict[key] = iri  # Keep original even if not found

# Print results
print(f"Total IRIs in dict: {len(random_words_map)}")
print(f"Found in RDF: {len(found_iris)}")
print(f"Replaced and found: {len(replaced_iris)}")
print(f"Missing from RDF: {len(missing_iris)}")

if replaced_iris:
    print("\nReplaced IRIs:")
    for key, old_iri, new_iri in replaced_iris:
        print(f"  Key {key}:")
        print(f"    Old: {old_iri}")
        print(f"    New: {new_iri}")

if missing_iris:
    print("\nMissing IRIs:")
    for key, iri in missing_iris:
        print(f"  Key {key}: {iri}")
else:
    print("\n✓ All IRIs found in the RDF file!")

# Write updated dictionary back to file
if replaced_iris:
    with open('randomClasses.py', 'w', encoding='utf-8') as f:
        f.write("random_words_map = {\n")
        for key in sorted(updated_dict.keys()):
            iri = updated_dict[key]
            f.write(f'    {key}: "{iri}",\n')
        f.write("}\n")
    
    print(f"\n✓ Updated random_classes.py with {len(replaced_iris)} corrected IRIs")
else:
    print("\n✓ No changes needed - dictionary file not modified")