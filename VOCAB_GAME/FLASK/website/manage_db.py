from . import db
from .models import DefinitionScores, UserDefinitions, UsedWord
from .models import Ontology as Ont
from owlready2 import *

import time

basedir = os.path.dirname(__file__)
def populate_definition_scores():
    """
    Populates the DefinitionScores based on the ontologies and their classes, and handles the removal of definitions
    that are not present in the ontology.
    """
    try:
        inicio = time.time()
        print('pop db')
        # Retrieve ontologies with non-null URLs
        ontologies = Ont.query.filter(Ont.ontology_url.isnot(None)).all()

        # Create a set to store all the definitions in the ontology
        all_definitions = set()

        for ontology in ontologies:
            ontology_path = os.path.join(basedir, "static", "ontologies",ontology.ontology_url)  # Retrieve the path to the selected ontology
            onto = get_ontology("file://" + ontology_path).load()
            classes = list(onto.classes()) # Get all the classes of the current selected ontology

            for owl_class in classes:

                class_name = owl_class.name
                comments = owl_class.comment

                if comments:  # Check if there are comments for the class

                    definition_score_default = DefinitionScores.query.filter_by(class_name=class_name,
                                                                          is_default=True).first()

                    if definition_score_default:
                        print('default')
                        db.session.delete(definition_score_default)
                        #db.session.commit()

                    for comment in comments:  # Process each comment

                        definition = str(comment)
                        definition_score = DefinitionScores.query.filter_by(class_name=class_name,
                                                                            definition=definition).first()

                        if definition_score is None: # Check if there is a default placeholder and update it with the actual definition

                        # Add the new definition and its score to the database
                            new_definition_score = DefinitionScores(class_name=class_name, definition=definition,
                                                                        score=0, agreements=0, is_default=False)
                            db.session.add(new_definition_score)  # Add the new definition and its score to the database
                            #db.session.commit()

                        all_definitions.add((owl_class.name, str(comment)))  # Add each definition to the set



                else:  # If no comments are available for the class, handle it accordingly
                    #print(class_name)
                    default_definition = "No definition available"  # Use a default placeholder for classes without specific definitions
                    definition_score = DefinitionScores.query.filter_by(class_name=class_name,
                                                                        definition=default_definition).first()

                    if definition_score is None: # Add the default definition and its score to the database
                        new_definition_score = DefinitionScores(class_name=class_name, definition=default_definition,
                                                                score=0, agreements=0, is_default=True)
                        db.session.add(new_definition_score)
                        #db.session.commit()
                        all_definitions.add((owl_class.name, str(default_definition)))

        # Retrieve all definitions in the database
        existing_definitions = DefinitionScores.query.all()

        # Find definitions in the database that are not in the ontology
        definitions_to_remove = [definition for definition in existing_definitions if
                                 (definition.class_name, definition.definition) not in all_definitions]

        # Remove definitions that are not in the ontology
        for definition in definitions_to_remove:
            if not definition.is_default:
                db.session.delete(definition)  # Delete the definition from the database
                #db.session.commit()

        # Commit the changes to the database
        db.session.commit()

        fin = time.time()
        tiempo_ejecucion = fin - inicio
        print("----------------------")
        print("Tiempo de ejecución: ")
        print(tiempo_ejecucion)
        print("----------------------")
        print("----------------------")

    except Exception as e:
        # Log the error and handle it accordingly
        print(f"An error occurred: {e}")
        db.session.rollback()
        # Additional error handling code as per the specific requirements


def remove_duplicate_definition_db():
    """
    Remove duplicate definitions from the database.
    """
    # Retrieve all definition scores from the database
    definition_scores = DefinitionScores.query.all()

    # Remove duplicate definitions
    for definition in definition_scores:
        for definition_2 in definition_scores:
            if definition.id != definition_2.id:
                if definition.definition == definition_2.definition:
                    db.session.delete(definition_2) # Delete the duplicate definition from the database

    # Commit the changes to the database
    db.session.commit()

def remove_previous_entries(profile_id):
    """
    Remove previous entries related to a specific profile from the UserDefinitions and UsedWord tables.

    Args:
    profile_id: The ID of the profile for which previous entries are to be removed.

    Returns:
    None
    """
    # Remove previous definitions
    previous_definitions = UserDefinitions.query.filter_by(profile_id=profile_id)
    if previous_definitions:
        for definition in previous_definitions:
            db.session.delete(definition)
        db.session.commit()
    # Remove previous used words
    previous_words = UsedWord.query.filter_by(profile_id=profile_id)
    if previous_words:
        for word in previous_words:
            db.session.delete(word)
        db.session.commit()

