import os
from owlready2 import get_ontology

# Configuración de las carpetas de entrada y salida
input_dir =     "C:/Users/UribelarreaJ/Desktop/OntoQuest/VOCAB_GAME/Ontology_Updater/raw_ontologies/un-processed"
output_dir =    "C:/Users/UribelarreaJ/Desktop/OntoQuest/VOCAB_GAME/Ontology_Updater/raw_ontologies/processed"

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file has an .owl extension
    if filename.endswith('.owl'):
        # Create the output filename by replacing .owl with .rdf
        output_filename = filename.replace('.owl', '.rdf')
        
        # Load the OWL file using owlready2
        onto = get_ontology(os.path.join(input_dir, filename)).load()
        
        # Save the ontology to an RDF file
        with open(os.path.join(output_dir, output_filename), 'wb') as f:
            onto.save(file=f, format='rdfxml')
        
        # Remove the processed file from the input directory
        os.remove(os.path.join(input_dir, filename))
