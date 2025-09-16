import logging
import owlready2
from flask import Blueprint, render_template, url_for, request, jsonify, redirect, flash
from flask_login import login_required, current_user
from flask import session
from .models import Profile, DepartmentOntologyAssociation, GameInformation, UserDefinitions, UsedWord, ExtendedUserDefinitions
from random import *
import random
import networkx as nx
from .manage_db import *
import json
from sqlalchemy import or_
from .definition_score import *
import os
from rdflib import RDFS
from .randomClasses import random_words_map

views = Blueprint('views', __name__)
basedir = os.path.dirname(__file__)

persistence_variable = []

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    remove_previous_entries(current_user.id) # Remove definitions and used words of the previous game

    #leaderboard_profiles = Profile.query.order_by(Profile.xp.desc()).limit(3).all() # Retrieve the top 3 leaderboard profiles
    #update_level_progression() # Update the level of all the profiles

    # Handle POST request for updating profile picture
    
    #if request.method == 'POST':
    #    if 'src' in request.json:
    #        src = request.json['src']
    #        src_parts = src.split('/')
    #        profile_picture = '/'.join(src_parts[src_parts.index('picture'):])
    #        user_profile = Profile.query.filter_by(user_id=current_user.id).first()
    #        if user_profile:
    #            user_profile.profile_picture = profile_picture  # Update the user's profile picture in the database
    #            db.session.commit()
    #            return jsonify({'message': 'Profile picture updated successfully'}) # Return success message
    
    # Render home page with user information if authenticated
    if current_user.is_authenticated:

        user_profile = Profile.query.filter_by(user_id=current_user.id).first() # Retrieve the user's profile
        if user_profile:

            #user_profile.level = level_progression(user_profile.xp) # Update user's profile level
            db.session.commit()
            # Retrieve necessary user's information for the home page
            username = user_profile.username
            #level = user_profile.level
            #xp = user_profile.xp
            #xp_percentage, xp_level, xp_to_reach = calculate_xp_percentage(level, xp) # Calculates different level information for the home page
            profile_picture = user_profile.profile_picture  # Retrieve the profile picture from the database

            # Render home page with user information
            return render_template('home.html', username=username, profile_picture=profile_picture)

    # Render home page with current user (if not authenticated)
    return render_template("home.html", user=current_user)

@views.route('/information', methods=['GET', 'POST'])
@login_required
def information():
    """
        Renders the information page of the game with a guide on how to play.

        Args:
        - None

        Returns:
        - Rendered template for the information page with the current user
        """
    # Render information page with the current user
    return render_template("information.html", user=current_user)

"""
@views.route('/leaderboard', methods=['GET', 'POST'])
@login_required
def leaderboard():

    leaderboard_profiles = Profile.query.order_by(Profile.xp.desc()).limit(3).all() # Retrieve the top 3 leaderboard profiles
    update_level_progression() # Update the level of all the profiles

    # Render home page with user information if authenticated
    if current_user.is_authenticated:

        user_profile = Profile.query.filter_by(user_id=current_user.id).first() # Retrieve the user's profile
        if user_profile:

            user_profile.level = level_progression(user_profile.xp) # Update user's profile level
            db.session.commit()
            # Retrieve necessary user's information for the home page
            username = user_profile.username
            level = user_profile.level
            xp = user_profile.xp
            xp_percentage, xp_level, xp_to_reach = calculate_xp_percentage(level, xp) # Calculates different level information for the home page
            profile_picture = user_profile.profile_picture  # Retrieve the profile picture from the database

            # Render home page with user information
            return render_template('leaderboard.html', username=username, level=level, profile_picture=profile_picture,
                                   xp_percentage=xp_percentage, xp_level=xp_level, xp_to_reach=xp_to_reach, leaderboard_profiles=leaderboard_profiles)

    # Render home page with current user (if not authenticated)
    return render_template("leaderboard.html", user=current_user)

@views.route('/challenges', methods=['GET', 'POST'])
@login_required
def challenges():

    leaderboard_profiles = Profile.query.order_by(Profile.xp.desc()).limit(3).all() # Retrieve the top 3 leaderboard profiles
    update_level_progression() # Update the level of all the profiles

    # Render home page with user information if authenticated
    if current_user.is_authenticated:

        user_profile = Profile.query.filter_by(user_id=current_user.id).first() # Retrieve the user's profile
        if user_profile:

            user_profile.level = level_progression(user_profile.xp) # Update user's profile level
            db.session.commit()
            # Retrieve necessary user's information for the home page
            username = user_profile.username
            level = user_profile.level
            xp = user_profile.xp
            xp_percentage, xp_level, xp_to_reach = calculate_xp_percentage(level, xp) # Calculates different level information for the home page
            profile_picture = user_profile.profile_picture  # Retrieve the profile picture from the database

            # Render home page with user information
            return render_template('challenges.html', username=username, level=level, profile_picture=profile_picture,
                                   xp_percentage=xp_percentage, xp_level=xp_level, xp_to_reach=xp_to_reach, leaderboard_profiles=leaderboard_profiles)

    # Render home page with current user (if not authenticated)
    return render_template("challenges.html", user=current_user)
"""

def update_level_progression():
    """
    Update the level progression for all user profiles based on their experience points (xp).

    Returns:
    None
    """
    user_profiles = Profile.query.all() # Retrieve all user profiles
    for profile in user_profiles:
        profile.level = level_progression(profile.xp) # Update the level based on the experience points
        db.session.commit() # Commit the changes to the database

# Calculate the xp percentage
def calculate_xp_percentage(level, xp):
    """
    Calculate the percentage of experience points achieved towards the next level and the current xp within the level.

    Args:
    level: The current level of the user.
    xp: The total experience points of the user.

    Returns:
    A tuple containing the xp percentage towards the next level, current xp within the level, and the xp to reach the next level.
    """
    xp_to_reach = (level+1)*100 # Calculate the total xp required to reach the next level
    n = sum(i * 100 for i in range(level + 1))  # Calculate the total xp achieved up to the current level
    xp_level = xp - n # Calculate the current xp within the level
    xp_percentage = (xp_level * 100) / xp_to_reach # Calculate the xp percentage towards the next level

    return xp_percentage, xp_level, xp_to_reach # Return the calculated values as a tuple


@views.route('/department', methods=['GET', 'POST'])
@login_required
def department():
    """
    Handle the selection of a department and update the user's game information.

    For GET requests, renders the department page with the current user.
    For POST requests, handles the department selection and updates the user's game information.

    Returns:
    If successful, redirects to the ontology selection page. Otherwise, renders the department page with appropriate messages.
    """
    #remove_duplicate_definition_db() # Remove duplicate definitions from the database
    #populate_definition_scores() # Populate definition scores database
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first() # Retrieve the user's game information

    # Handle POST request for department selection
    if request.method == 'POST':
        selected_department = request.form['departments']
        # Validate the selected department
        if selected_department == "":
            flash('Please select a valid department.', category='error')
        # Update the user's game information if a department is selected
        elif profile_game is not None:  # If the user already has a game information record, update it
            profile_game.department = selected_department
            db.session.commit()
            return redirect(url_for('views.ontology_selection'))

        else:  # If no, create a new game information record
            new_game = GameInformation(profile_id=current_user.id, department=selected_department)
            db.session.add(new_game)
            db.session.commit()
            return redirect(url_for('views.ontology_selection'))
    # Render department page with current user for GET requests
    return render_template("department.html", user=current_user)


@views.route('/ontology-selection', methods=['GET', 'POST'])
@login_required
def ontology_selection():
    """
    Handle the ontology selection process based on the user's department.

    For GET requests, retrieves relevant ontologies based on the user's department and renders the ontology selection page.
    For POST requests, processes the user's ontology selection, updates the user's game information, and redirects to the next step.

    Returns:
    If successful, redirects to the number question page. Otherwise, renders the ontology selection page with appropriate messages.
    """
    #remove_duplicate_definition_db()  # Remove duplicate definitions from the database
    #populate_definition_scores()  # Populate definition scores

    if current_user.is_authenticated:
        # Retrieve the user's game information
        profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()
        # Retrieve the user's department from the profile
        user_department = profile_game.department
        # Retrieve relevant ontologies based on the user's department
        relevant_ontology_associations = DepartmentOntologyAssociation.query.filter_by(department=user_department).all()

        # Extract the relevant ontologies from the associations
        relevant_ontologies = [association.ontology for association in relevant_ontology_associations]
        #print(relevant_ontologies)
        # Convert the ontologies to a JSON-compatible list for rendering on the front-end
        ontologies_json = create_ontology_json(relevant_ontologies)

        if request.method == 'POST':
            # Process the user's ontology selection
            selected_ontology_id = request.form['selectedOntologyId']
            ont = Ont.query.filter_by(id=selected_ontology_id).first()
            if selected_ontology_id:
                if not ont.ontology_url:
                    flash('Please select another Ontology.', category='error')
                else: # Update the user's game information with the selected ontology
                    profile_game.ontology_id = selected_ontology_id
                    db.session.commit()
                    return redirect(url_for('views.number_question')) # Redirect to the next step after successful ontology selection
            else:
                flash('Ontology Not Found.', category='error')

        # Render the ontology selection page with the relevant ontologies
        return render_template("ontology-selection.html", user=current_user, ontologies_json=ontologies_json, ontologies=relevant_ontologies)


def create_ontology_json(relevant_ontologies):
    """
    Create a JSON representation of relevant ontologies.

    Args:
    relevant_ontologies: A list of relevant ontology objects.

    Returns:
    A list of JSON objects representing the relevant ontologies.
    """
    ontologies_json = [] # Initialize a list to store the JSON representations of relevant ontologies
    for ontology in relevant_ontologies:
        # Create a JSON object for each relevant ontology
        ontology_data = {
            'id': ontology.id,
            'name': ontology.name,
            'description': ontology.description,
            'image_url': url_for('static', filename=ontology.image_url)  # Generate the image URL
        }
        ontologies_json.append(ontology_data) # Append the JSON representation to the list
    return ontologies_json # Return the list of JSON representations of relevant ontologies


@views.route('/number-question', methods=['GET', 'POST'])
@login_required
def number_question():
    """
    Handle the selection of the number of questions for the user's game.

    For GET requests, renders the number question page for the user to select the number of questions.
    For POST requests, updates the user's game information with the selected number of questions and redirects to the first question.

    Returns:
    If successful, redirects to the question handling page. Otherwise, renders the number question page with appropriate messages.
    """
    #remove_duplicate_definition_db()  # Remove duplicate definitions from the database
    #populate_definition_scores()  # Populate definition scores
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()  # Retrieve the user's game information
    ontology_selected, ontology_path, onto, classes = get_ontology_information(profile_game)  # Retrieve ontology information

    if current_user.is_authenticated:
        profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()

        if request.method == 'POST':
            # Process the user's selection of the number of questions
            number_question = request.form['numberRange']

            if int(number_question) > len(classes):
                flash('Please select a number of questions that is equal to or less than the total number of terms available in the selected ontology.', category='error')

            else:
                profile_game.num_questions = number_question # Update the user's game information with the number of questions
                db.session.commit()
                # Redirect to the first question of the game after successful update of the number of questions
                return redirect(url_for('views.handle_question', question_number=1))

    # Render the number question page for the user to select the number of questions
    return render_template("number-question.html", user=current_user)


def construct_graph(random_word, onto):
    """
    Construct a directed graph representing the relationships between a selected class and other classes and properties within an ontology.

    Args:
    random_word: The selected class from the ontology.
    onto: The ontology containing the classes and properties.

    Returns:
    A directed graph (DiGraph) representing the relationships between the selected class and other classes and properties.
    """
    G = nx.DiGraph() # Initialize a directed graph


    # Add the selected class (random word) to the graph
    G.add_node(random_word.name, name=random_word.name, definition=get_highest_scored_definition(random_word), type="owl:Class")

    # Add edges for the selected class (random word), its subclasses and superclasses, and their relationships
    for cls in onto.classes():
        if random_word in cls.is_a:
            G.add_node(cls.name, name=cls.name, definition=get_highest_scored_definition(cls), type="owl:Class")  # Add the superclass as a node
            G.add_edge(cls.name, random_word.name, label="Subclass of", type="subclass")  # Add edge for subclass relationship
        if cls in random_word.is_a:
            G.add_node(cls.name, name=cls.name, definition=get_highest_scored_definition(cls), type="owl:Class")  # Add the subclass as a node
            G.add_edge(random_word.name, cls.name, label="Subclass of",type="subclass" )  # Add edge for superclass relationship

        
        #for prop in onto.object_properties(): # Add the object properties of the random word
            for domain_cls in prop.domain:
                if domain_cls == random_word:
                    for range_cls in prop.range:
                        G.add_node(range_cls.name, name=range_cls.name, definition=get_highest_scored_definition(range_cls),
                                    type="owl:Class")
                        G.add_edge(random_word.name, range_cls.name, label=prop.name, type="objectproperties")
            for range_cls in prop.range:
                if range_cls == random_word:
                    for domain_cls in prop.domain:
                        G.add_node(domain_cls.name, name=domain_cls.name, definition=get_highest_scored_definition(domain_cls),
                                    type="owl:Class")
                        G.add_edge(domain_cls.name, random_word.name, label=prop.name, type="objectproperties")
        """
        for prop in onto.object_properties(): # Add the object properties of the random word
            for domain_cls in prop.domain:
                if domain_cls == random_word:
                    for range_cls in prop.range:
                        if hasattr(range_cls, 'name'):
                            G.add_node(range_cls.name, name=range_cls.name, definition=get_highest_scored_definition(range_cls), type="owl:Class")
                            G.add_edge(random_word.name, range_cls.name, label=prop.name, type="objectproperties")
                        else:
                            if isinstance(range_cls, Or):
                                # Handling case where range_cls is of type 'Or'
                                print(f"Warning: Logical combination detected in range_cls - {range_cls}")
                            else:
                                print(f"Error: range_cls doesn't have 'name' attribute")

            for range_cls in prop.range:
                if range_cls == random_word:
                    for domain_cls in prop.domain:
                        if hasattr(domain_cls, 'name'):
                            G.add_node(domain_cls.name, name=domain_cls.name, definition=get_highest_scored_definition(domain_cls), type="owl:Class")
                            G.add_edge(domain_cls.name, random_word.name, label=prop.name, type="objectproperties")
                        else:
                            if isinstance(domain_cls, Or):
                                # Handling case where domain_cls is of type 'Or'
                                print(f"Warning: Logical combination detected in domain_cls - {domain_cls}")
                            else:
                                print(f"Error: domain_cls doesn't have 'name' attribute")
        """
        for prop in onto.data_properties(): # Add the data properties of the random word
            for domain_cls in prop.domain:
                if domain_cls == random_word:
                    for range_cls in prop.range:
                        range_str = str(range_cls)  # Convert to string representation
                        try:
                            data_type = range_str.split("'")[1]  # Extract the datatype from the string representation
                        except IndexError:
                            data_Type = None
                        unique_data_type = f"{data_type}_{id(prop)}"  # Create a unique identifier for each data type
                        G.add_node(unique_data_type, name=data_type, definition="", type="owl:DatatypeProperty")  # Add a node for the unique data property type
                        G.add_edge(random_word.name, unique_data_type, label=prop.name, type="dataproperties")

    return G # Return the constructed directed graph

def construct_ontology_graph(onto):
    """
    Construct a directed graph representing the relationships between classes and properties within an ontology.

    Args:
    onto: The ontology containing the classes and properties.

    Returns:
    A directed graph (DiGraph) representing the relationships between classes and properties in the ontology.
    """
    G = nx.DiGraph()  # Initialize a directed graph

    # Iterate over all classes in the ontology
    for cls in onto.classes():
        G.add_node(cls.name, name=cls.name, definition=get_highest_scored_definition(cls), type="owl:Class")  # Add the class as a node
        for parent_cls in cls.is_a:
            if parent_cls in onto.classes():
                G.add_edge(parent_cls.name, cls.name, label="Subclass of", type="subclass")  # Add edge for subclass relationship

    # Iterate over all the object properties in the ontology
    for prop in onto.object_properties():
        for domain_cls in prop.domain:
            for range_cls in prop.range:
                    G.add_edge(domain_cls.name, range_cls.name, label=prop.name, type="objectproperties")

    # Iterate over all the data properties in the ontology
    for prop in onto.data_properties():
        for domain_cls in prop.domain:
            for range_cls in prop.range:
                range_str = str(range_cls)  # Convert to string representation
                data_type = range_str.split("'")[1]  # Extract the datatype from the string representation
                unique_data_type = f"{data_type}_{id(prop)}"  # Create a unique identifier for each data type
                print(data_type)
                G.add_node(unique_data_type,name=data_type, definition="",
                           type="owl:DatatypeProperty")  # Add a node for the unique data property type
                G.add_edge(domain_cls.name, unique_data_type, label=prop.name, type="dataproperties")

    return G  # Return the constructed directed graph

def create_ontology_file(random_word, onto):
    """
    Create an ontology (RDF file) representing the relationships between a selected class and other classes and properties using Owlready2.

    Args:
    random_word: The selected class from the ontology.
    onto: The ontology from which the random word is extracted.

    Returns:
    None
    """


    file_path = os.path.join(basedir, "static", "ontologies", "YOUR_ONTOLOGY.rdf")
    print(file_path)
    if os.path.exists(file_path):
        new_onto = get_ontology("file://" + file_path).load()  # Load the ontology using its path
        new_onto.destroy()
        os.remove(file_path)
        print('removed')

    if not os.path.exists(file_path):
        open(file_path, "w")
        print('created')

    new_onto = get_ontology("file://" + file_path).load()  # Load the ontology using its path

    class_dict = {}
    with new_onto:
        class_dict.update({random_word.name: types.new_class(random_word.name, (Thing,))})
        for cls in onto.classes():

            if cls in random_word.is_a:
                random_class = class_dict[random_word.name]
                if owl.Thing in random_class.is_a:
                    random_class.is_a.remove(owl.Thing)
                class_dict.update({cls.name: types.new_class(cls.name, (Thing,))})
                random_class.is_a.append(class_dict[cls.name])
            if random_word in cls.is_a:
                class_dict.update({cls.name: types.new_class(cls.name, (class_dict[random_word.name],))})
                current_class = class_dict[cls.name]
                current_class.is_a.append(class_dict[random_word.name])

            for prop in onto.properties():
                if cls in prop.domain and random_word in prop.range:  # Case where the selected class is the range of a property
                    if not cls.name in class_dict:
                        class_dict.update({cls.name: types.new_class(cls.name, (Thing,))})
                    new_prop = types.new_class(prop.name, (ObjectProperty,))
                    new_prop.domain = [class_dict[cls.name]]
                    new_prop.range = [class_dict[random_word.name]]
                if random_word in prop.domain and cls in prop.range:  # Case where the selected class is the domain of a property
                    if not cls.name in class_dict:
                        class_dict.update({cls.name: types.new_class(cls.name, (Thing,))})
                    new_prop = types.new_class(prop.name, (ObjectProperty,))
                    new_prop.domain = [class_dict[random_word.name]]
                    new_prop.range = [class_dict[cls.name]]

    # Save the ontology to a file
    new_onto.save(file_path, format="rdfxml")
    print('new ontology')




def select_random_word(classes, previous_used_classes):
    """
    Select a random word from the available classes, excluding any classes that have been previously used.

    Args:
    classes: A list of available classes.
    previous_used_classes: A list of classes that have been previously used.

    Returns:
    The randomly selected word from the available classes.
    """
    available_words = [c for c in classes if c not in previous_used_classes] # Filter out previously used classes
    random_word = choice(available_words) # Select a random word from the available classes

    return random_word # Return the randomly selected word


def store_used_word(random_word, profile_id):
    """
    Store the used word in the database for the given user profile.

    Args:
    random_word: The word to be stored in the database.
    profile_id: The ID of the user profile.

    Returns:
    None
    """
    try:
        # Prüfen, ob random_word oder random_word.iri None ist, bevor versucht wird, es zu verwenden
        if random_word is None or random_word.iri is None:
            raise ValueError("The word or its IRI is None and cannot be added to the database.")

        # Create a new record for the used word
        used_word_record = UsedWord(profile_id=profile_id, word_uri=random_word.iri)
        db.session.add(used_word_record)  # Add the record to the database session
        db.session.commit()  # Commit the transaction to the database

    except ValueError as ve:
        # Behandlung für den Fall, dass random_word oder dessen IRI None ist
        print(f"ValueError: {ve}")
        # Optional: Logging oder alternative Logik hinzufügen

    except Exception as e:
        # Allgemeine Fehlerbehandlung
        print(f"An unexpected error occurred: {e}")
        # Optional: Rollback der Transaktion durchführen, um inkonsistente Zustände zu vermeiden
        db.session.rollback()


def get_previous_used_classes(profile_id, ontology_path):
    """
    Retrieve the previous used classes (words) for a given user profile from the database.

    Args:
    profile_id: The ID of the user profile.
    ontology_path: The path to the ontology.

    Returns:
    A list of previous used classes for the user profile.
    """
    previous_used_words = UsedWord.query.filter_by(profile_id=profile_id).all()  # Retrieve previous used words from the database
    previous_used_classes = [used_word_record.get_word(ontology_path) for used_word_record in previous_used_words]  # Extract the classes from the used words


    # Return the list of previous used classes
    return previous_used_classes


def get_ontology_information(profile_game):
    """
    Retrieve ontology information based on the user's selected ontology.

    Args:
    profile_game: The user's game information including the selected ontology.

    Returns:
    A tuple containing the selected ontology, its path, the ontology object, and a list of its classes.
    """
    ontology_selected = profile_game.ontology # Retrieve the user's selected ontology

    ontology_path = os.path.join(basedir, "static", "ontologies", ontology_selected.ontology_url) # Retrieve the path to the selected ontology
    onto = get_ontology("file://" + ontology_path).load() # Load the ontology using its path
    classes = list(onto.classes()) # Retrieve a list of classes from the ontology

    return ontology_selected, ontology_path, onto, classes # Return the retrieved ontology information


@views.route('/game/question/visualization', methods=['GET', 'POST'])
@login_required
def term_visualization():
    """
    Route for visualizing a term and its relations in the ontology graph.

    Upon accessing this route, the current user's game information and ontology details are retrieved.
    The visualization of a random word and its associated information is prepared for display.

    Args:
    - None

    Returns:
    - Rendered template for term visualization with relevant data and graph for presentation
    """
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()  # Retrieve the user's game information
    ontology_selected, ontology_path, onto, classes = get_ontology_information(profile_game)  # Retrieve ontology information
    random_word = None

    if request.method == 'GET':
        random_word_name = profile_game.random_word  # Retrieve the current random word from the user's game information
        highest_scored_definition = profile_game.random_definition  # Retrieve the highest scored definition

        for cls in onto.classes():
            if cls.name == random_word_name:
                random_word = cls

        G = construct_graph(random_word, onto)  # Construct a graph based on the random word and ontology
        graph_json = nx.node_link_data(G)  # Convert the graph to JSON format for visualization
        graph_json = json.dumps(graph_json)  # Serialize the graph JSON data

        # Load the ontology using its path and retrieve classes, object properties, superclass, and subclass information
        class_onto = create_ontology_file(random_word, onto)
        file_path= os.path.join(basedir, "static", "ontologies", "DigitalReference.rdf")
        onto_word = get_ontology("file://" + file_path).load()  # Load the ontology using its path
        classes = list(onto_word.classes())

        object_properties = list(onto_word.object_properties())
        number_classes = len(classes) - 1
        number_object_properties = len(object_properties)
        number_superclasses = 0
        number_subclasses = 0

        for cls in onto.classes():
            if cls in random_word.is_a:
                number_superclasses += 1
            if random_word in cls.is_a:
                number_subclasses += 1

        name = random_word.name.replace("_", " ")
        return render_template('term-visualization.html', user=current_user, word=name, definition=highest_scored_definition,
                               ontology_graph=graph_json, onto_id=ontology_selected.id, number_classes=number_classes, number_object_properties=number_object_properties,
                               number_superclasses=number_superclasses, number_subclasses=number_subclasses)

    return render_template('term-visualization.html', user=current_user)

@views.route('/game/question/mobile-visualization', methods=['GET', 'POST'])
@login_required
def mobile_term_visualization():
    """
    Route for visualizing a term and its relations in the ontology graph (mobile version).

    This function retrieves the current user's game information and ontology details and prepares the visualization of a random word and its associated information for display on mobile devices.

    Args:
    - None

    Returns:
    - Rendered template for mobile term visualization with relevant data and graph for presentation
    """
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()  # Retrieve the user's game information
    ontology_selected, ontology_path, onto, classes = get_ontology_information(profile_game)  # Retrieve ontology information
    random_word = None

    if request.method == 'GET':
        random_word_name = profile_game.random_word  # Retrieve the current random word from the user's game information
        highest_scored_definition = profile_game.random_definition  # Retrieve the highest scored definition

        for cls in onto.classes():
            if cls.name == random_word_name:
                random_word = cls

        G = construct_graph(random_word, onto)  # Construct a graph based on the random word and ontology
        graph_json = nx.node_link_data(G)  # Convert the graph to JSON format for visualization
        graph_json = json.dumps(graph_json)  # Serialize the graph JSON data

        # Load the ontology using its path and retrieve classes, object properties, superclass, and subclass information
        class_onto = create_ontology_file(random_word, onto)
        file_path = os.path.join(basedir, "static", "ontologies", "YOUR_ONTOLOGY.rdf")
        onto_word = get_ontology("file://" + file_path).load()  # Load the ontology using its path  # Load the ontology using its path
        classes = list(onto_word.classes())

        object_properties = list(onto_word.object_properties())
        number_classes = len(classes) - 1
        number_object_properties = len(object_properties)
        number_superclasses = 0
        number_subclasses = 0

        for cls in onto.classes():
            if cls in random_word.is_a:
                number_superclasses += 1
            if random_word in cls.is_a:
                number_subclasses += 1


        return render_template('mobile-term-visualization.html', user=current_user, word=random_word.name, definition=highest_scored_definition,
                               ontology_graph=graph_json, onto_id=ontology_selected.id, number_classes=number_classes, number_object_properties=number_object_properties,
                               number_superclasses=number_superclasses, number_subclasses=number_subclasses)

    return render_template('mobile-term-visualization.html', user=current_user)

@views.route('/game/summary/visualization', methods=['GET', 'POST'])
@login_required
def ontology_visualization():
    """
    Route for visualizing an entire ontology.

    This function retrieves the current user's game information and ontology details and prepares the visualization of the ontology graph for display.

    Args:
    - None

    Returns:
    - Rendered template for ontology visualization with relevant data and graph for presentation
    """
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()  # Retrieve the user's game information
    ontology_selected, ontology_path, onto, classes = get_ontology_information(profile_game)  # Retrieve ontology information

    # Retrieve the ontology name, description, construct a graph, and convert it to JSON format for visualization
    if request.method == 'GET':

        onto_name = ontology_selected.name
        onto_description = ontology_selected.description

        G = construct_ontology_graph(onto)  # Construct a graph based on the random word and ontology
        graph_json = nx.node_link_data(G)  # Convert the graph to JSON format for visualization
        graph_json = json.dumps(graph_json)  # Serialize the graph JSON data

        classes = list(onto.classes()) # Retrieve classes from the ontology
        object_properties = list(onto.object_properties()) # Retrieve object properties from the ontology
        data_properties = list(onto.data_properties())  # Retrieve data properties from the ontology
        number_classes = len(classes) # Calculate the number of classes
        number_object_properties = len(object_properties) # Calculate the number of object properties
        number_data_properties = len(object_properties)  # Calculate the number of data properties

        # Render the template with the retrieved data for ontology visualization
        return render_template('ontology-visualization.html', user=current_user, onto_name=onto_name, onto_description=onto_description,  ontology_graph=graph_json, onto_id=ontology_selected.id, number_classes=number_classes, number_object_properties=number_object_properties,
                               number_data_properties=number_data_properties)

    return render_template('ontology-visualization.html', user=current_user)

@views.route('/game/summary/mobile-visualization', methods=['GET', 'POST'])
@login_required
def mobile_ontology_visualization():
    """
    Route for visualizing an entire ontology (mobile version).

    This function retrieves the current user's game information and ontology details and prepares the mobile visualization of the ontology graph for display.

    Args:
    - None

    Returns:
    - Rendered template for mobile ontology visualization with relevant data and graph for presentation
    """
    # Retrieve the user's game information and ontology details
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()  # Retrieve the user's game information
    ontology_selected, ontology_path, onto, classes = get_ontology_information(profile_game)  # Retrieve ontology information

    # Retrieve the ontology name, description, construct a graph, and convert it to JSON format for visualization
    if request.method == 'GET':

        onto_name = ontology_selected.name
        onto_description = ontology_selected.description

        G = construct_ontology_graph(onto)  # Construct a graph based on the random word and ontology
        graph_json = nx.node_link_data(G)  # Convert the graph to JSON format for visualization
        graph_json = json.dumps(graph_json)  # Serialize the graph JSON data

        classes = list(onto.classes())  # Retrieve classes from the ontology
        object_properties = list(onto.object_properties())  # Retrieve object properties from the ontology
        number_classes = len(classes)  # Calculate the number of classes
        number_object_properties = len(object_properties)  # Calculate the number of object properties

        # Render the template with the retrieved data for ontology visualization
        return render_template('mobile-ontology-visualization.html', user=current_user, onto_name=onto_name, onto_description=onto_description,  ontology_graph=graph_json, onto_id=ontology_selected.id, number_classes=number_classes, number_object_properties=number_object_properties,
                               )

    return render_template('mobile-ontology-visualization.html', user=current_user)

def get_definition_from_ontology(class_name):
    # Ruta a tu ontología
    ontology_path = "ruta/a/tu/ontologia.owl"
    
    # Cargar la ontología
    onto = get_ontology("file://" + ontology_path).load()
    
    # Buscar la clase en la ontología
    for owl_class in onto.classes():
        if owl_class.name == class_name:
            # Obtener el comentario (definición)
            if owl_class.comment:
                return str(owl_class.comment[0])  # Asumiendo que hay un solo comentario por clase
            else:
                return "No definition available"

@views.route('/game/question/<int:question_number>', methods=['GET', 'POST'])
@login_required
def handle_question(question_number):
    """
    Handle the questions in the game based on the user's interactions and responses.

    For GET requests, retrieves ontology information, selects a random word, and renders the question interface.
    For POST requests, processes the user's response, updates the database, and redirects to the next step or summary page.

    Returns:
    If successful, redirects to the next question or summary page. Otherwise, renders the question interface.
    """
    #remove_duplicate_definition_db()  # Remove duplicate definitions from the database
    #populate_definition_scores()  # Populate definition scores
    
    

    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()  # Retrieve the user's game information
    ontology_selected, ontology_path, onto, classes = get_ontology_information(profile_game)  # Retrieve ontology information
    fixed_words_map = {
        1: next(cls for cls in classes if cls.iri == "http://www.w3id.org/ecsel-dr-DF#Supply_Chain"),
        2: next(cls for cls in classes if cls.iri == "http://www.w3id.org/ecsel-dr-BMS#Semiconductor_Company"),
        3: next(cls for cls in classes if cls.iri == "http://www.w3id.org/ecsel-dr-SO#Fab"),
        4: next(cls for cls in classes if cls.iri == "http://www.w3id.org/ecsel-dr-GDM#Equipment"),
        5: next(cls for cls in classes if cls.iri == "http://www.w3id.org/ecsel-dr-GDM#Calendar")
    }
    
    if question_number == 1 and request.method == 'GET': # Means the user started a new game, reset the previous game's information
        remove_previous_entries(current_user.id) # Remove previous entries for the current user
    if request.method == 'GET':

        previous_used_classes = get_previous_used_classes(current_user.id, ontology_path) # Retrieve previous used classes in the last questions
        random_word = select_random_word(classes, previous_used_classes) # Select a random word (class) to be displayed
        if question_number <= 5:
            random_word = fixed_words_map.get(question_number)
        elif question_number > 5:
            #random_word = random_words_map.get(random.randint(1, 178))
            iri = random_words_map.get(random.randint(16, 349))
            random_word = next(cls for cls in classes if cls.iri == iri)
            print(iri)
            while random_word in previous_used_classes:
                #random_word = random_words_map.get(random.randint(1, 178))
                iri = random_words_map.get(random.randint(16, 349))
                random_word = next(cls for cls in classes if cls.iri == iri)
                print(iri)
        store_used_word(random_word, current_user.id) #Store the used word in the database
        try:
            definition = get_highest_scored_definition(random_word) # Retrieve the highest scored definition associated to the random word
        except ValueError as e:
            print (f"Error when loading definition: {e}")
            definition = None
        profile_game.random_word = random_word.name # Update the user's game information with the current random word
        profile_game.random_definition = definition
        db.session.commit() # Commit the updates to the database

        G = construct_graph(random_word, onto) # Construct a graph based on the random word and ontology
        graph_json = nx.node_link_data(G) # Convert the graph to JSON format for visualization
        graph_json = json.dumps(graph_json) # Serialize the graph JSON data

        total_question = profile_game.num_questions # Retrieve the total number of questions selected by the user
        rounded_percentage = round(question_number * 100 / total_question) # Calculate the percentage progress of the game

        # Retrieve additional information for rendering the question interface
        #alternative_names = getattr(random_word, 'hasAlternativeName', ['N/A'])  # If no alternative names, default to 'N/A'
        alternative_names = ['N/A']
        abbreviations = ['N/A']
        examples = ['N/A']
        #abbreviations = getattr(random_word, 'hasAbbreviation', ['N/A'])  # If no abbreviations, default to 'N/A']
        # german_names = getattr(random_word, 'hasGermanName', ['N/A'])  # If no German names, default to 'N/A'
        #examples = getattr(random_word, 'hasExample', ['N/A'])  # If no examples, default to 'N/A']

        name = random_word.name.replace("_", " ")
        return render_template('handle-question.html', user=current_user, question_number=question_number,
                               word=name, definition=definition,
                               rounded_percentage=rounded_percentage, ontology_graph=graph_json,
                               onto_id=ontology_selected.id, alternative_names=alternative_names,
                               abbreviations=abbreviations, examples=examples)

    # Handle the user's response and perform appropriate actions based on the input
    elif request.method == 'POST':

        next_question_number = question_number + 1 # Calculate the number of the next question
        validation_response = request.form['validationResponse'] # Retrieve the user's validation response
        random_word = profile_game.random_word  # Retrieve the current random word from the user's game information
        highest_scored_definition = profile_game.random_definition # Retrieve the highest scored definition
        #print('profile word:', random_word)
        alternative_name = request.form.get('alternativeName') # Retrieve the alternative name input from the form
        abbreviation = request.form.get('abbreviation') # Retrieve the abbreviation input from the form
        #german_name = request.form.get('germanName') # Retrieve the German name input from the form
        example = request.form.get('example') # Retrieve the example input from the form

        # Update the ontology classes with the user-provided information
        for owl_class in classes:
            if owl_class.name == random_word:
                if alternative_name:
                    owl_class.hasAlternativeName.append(alternative_name)  # Add the alternative name to the class
                elif abbreviation:
                    owl_class.hasAbbreviation.append(abbreviation)  # Add the abbreviation to the class
                #elif german_name:
                #   owl_class.hasGermanName.append(german_name)  # Add the German name to the class
                elif example:
                    owl_class.hasExample.append(example)  # Add the example to the class

        onto.save(file=ontology_path, format="rdfxml") # Save the updates to the ontology file

        check_number_definition(random_word) # Check the number of definitions for the random word and performs action if necessary

        if validation_response == 'disagree':
            # Handle the behavior when the "false" button was initially clicked
            user_activity = UserDefinitions(profile_id=current_user.id, profile_class=random_word,
                                            profile_definition=highest_scored_definition) # Create a user activity record
            db.session.add(user_activity) # Add the user activity to the database session
            db.session.commit() # Commit the transaction to the database

            session['alternative_name'] = alternative_name
            session['abbreviation'] = abbreviation
            #session['german_name'] = german_name
            session['example'] = example
            extended_user_activity = ExtendedUserDefinitions(
            profile_id=current_user.id,
            profile_class=random_word,
            profile_definition=highest_scored_definition,
            action_type='disagree',
            #revised_definition=revised_definition,
            alternative_name=alternative_name,
            abbreviation=abbreviation,
            #german_name=german_name,
            example=example,
            ontology_iri=onto.base_iri)

            db.session.add(extended_user_activity)
            db.session.commit()



            return redirect(url_for('views.disagreement', question_number=question_number)) # Redirect to the disagreement page

        elif validation_response == 'agree':
            # Handle the behavior when the "true" button was initially clicked
            increase_score_for_definition(random_word, highest_scored_definition) # Increase the score for the definition

            user_activity = UserDefinitions(profile_id=current_user.id, profile_class=random_word,
                                            profile_definition=highest_scored_definition, action_type="agree") # Create a user activity record
            db.session.add(user_activity) # Add the user activity to the database session
            db.session.commit() # Commit the transaction to the database
            if question_number == profile_game.num_questions:
                # Redirect to the summary page if it's the last question
                return redirect(url_for('views.summary'))
            else:
                # Redirect to the next question
                return redirect(url_for('views.handle_question', question_number=next_question_number))

        elif validation_response == 'enter':
            # Handle the behavior if no current definition and the "Enter your own definition" button was initially clicked
            user_activity = UserDefinitions(profile_id=current_user.id, profile_class=random_word,
                                            profile_definition=highest_scored_definition) # Create a user activity record
            db.session.add(user_activity) # Add the user activity to the database session
            db.session.commit() # Commit the transaction to the database
            return redirect(url_for('views.enter_definition', question_number=question_number)) # Redirect to enter definition page

        elif validation_response == 'pass':
            # Handle the behavior when the "pass" button was clicked
            user_activity = UserDefinitions(profile_id=current_user.id, profile_class=random_word,
                                            profile_definition=highest_scored_definition, action_type="pass") # Create a user activity record
            db.session.add(user_activity) # Add the user activity to the database session
            db.session.commit() # Commit the transaction to the database
            if question_number == profile_game.num_questions:
                # Redirect to the summary page if it's the last question
                return redirect(url_for('views.summary'))
            else:
                # Redirect to the next question
                return redirect(url_for('views.handle_question', question_number=next_question_number))

    return render_template('handle-question.html', user=current_user, question_number=question_number)



@views.route('/game/question/<int:question_number>/disagreement', methods=['GET', 'POST'])
@login_required
def disagreement(question_number):
    """
    Handle user disagreements during the game for a specific question.

    For GET requests, retrieves relevant definitions and renders the disagreement interface.
    For POST requests, processes the user's selected definition, updates the database, and redirects to the next question or summary page.

    Returns:
    If successful, redirects to the next question or summary page. Otherwise, renders the disagreement interface.
    """
    next_question_number = question_number + 1  # Calculate the number of the next question
    populate_definition_scores()  # Populate definition scores
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()  # Retrieve the user's game information

    if request.method == 'GET':
        random_word = profile_game.random_word  # Retrieve the current random word from the user's game information
        random_definition = profile_game.random_definition  # Retrieve the current random definition from the user's game information

        current_definition = DefinitionScores.query.filter_by(class_name=random_word,
                                                              definition=random_definition).first() # Retrieve the current definition's scores

        # Retrieve relevant alternative definitions (definitions with high score) for the disagreement interface

        relevant_definitions = DefinitionScores.query.filter(DefinitionScores.score <= current_definition.score,
                                                             DefinitionScores.class_name == random_word,
                                                             DefinitionScores.definition != random_definition).order_by(DefinitionScores.score.desc()).limit(3).all()

        if not relevant_definitions: # Case where there is no other alternative definition for the selected word (class)
            no_alt ="There is currently no other alternative, but you can still enter your own definition to help improve the ontology."
            return render_template('disagreement.html', user=current_user, question_number=question_number,
                                   word=random_word, relevant_definitions=relevant_definitions,
                                   next_question_number=next_question_number, random_definition=random_definition, no_alt=no_alt)

        return render_template('disagreement.html', user=current_user, question_number=question_number,
                               word=random_word, relevant_definitions=relevant_definitions,
                               next_question_number=next_question_number, random_definition=random_definition)

    elif request.method == 'POST':

        selected_definition = request.form['selectedDefinition'] # Retrieve the user's selected definition
        # Calculate semantic similarity between the current high scored definition and the user's selected alternative definition
        semantic_similarity(profile_game.random_definition, selected_definition)

        # Decrease the score for the current high scored definition
        decrease_score_for_definition(profile_game.random_word, profile_game.random_definition, selected_definition)

        # Update the user's activity with the revised definition and action type
        user_activity = UserDefinitions.query.filter_by(profile_id=current_user.id,
                                                        profile_definition=profile_game.random_definition).first()
        user_activity.revised_definition = selected_definition
        user_activity.action_type = "selected"
        db.session.commit() # Commit the transaction to the database

        new_definition = DefinitionScores.query.filter_by(definition=selected_definition).first() # Retrieve the details for the selected new definition
        increase_score_for_definition(new_definition.class_name, new_definition.definition) # Increase the score for the new definition

        # Redirect to the summary page if it's the last question, otherwise redirect to the next question
        if question_number == profile_game.num_questions:

            return redirect(url_for('views.summary'))
        return redirect(url_for('views.handle_question', question_number=next_question_number))

    return render_template('disagreement.html', user=current_user, question_number=question_number)


@views.route('/game/question/<int:question_number>/enter-definition', methods=['GET', 'POST'])
@login_required
def enter_definition(question_number):
    """
    Handle the entry of user-defined definitions during the game for a specific question.

    For GET requests, renders the user interface to enter a definition.
    For POST requests, processes the entered or closest definitions, updates the database, and redirects to the next question or summary page.

    Returns:
    If successful, redirects to the next question or summary page. Otherwise, renders the user interface for entering a definition.
    """
    next_question_number = question_number + 1  # Calculate the number of the next question
    populate_definition_scores()  # Populate definition scores database
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()  # Retrieve the user's game information
    ontology_selected, ontology_path, onto, classes = get_ontology_information(profile_game)  # Retrieve ontology information
    random_word = profile_game.random_word  # Retrieve the current word for the question
    random_definition = profile_game.random_definition

    if request.method == 'GET':
        return render_template('enter-definition.html', user=current_user, question_number=question_number,
                               word=random_word, definition=random_definition)

    elif request.method == 'POST':
        entered_definition = request.form['selectedEnteredDefinition'] # Retrieve the user-entered definition from the form
        closest_definition = request.form['selectedClosestDefinition'] # Retrieve the closest definition selected by the user from the form

        print('closest def:', closest_definition)
        print('entered def:', entered_definition)

        # Process the entered or closest definitions and update the database accordingly
        if entered_definition: # Handle the user's entered definition
            # Decrease the score for the current high scored definition
            decrease_score_for_definition(profile_game.random_word, profile_game.random_definition, entered_definition)

            # Add the entered definition to the score database
            new_definition = DefinitionScores(class_name=random_word, definition=entered_definition, score=1, agreements=1) # Create a new definition score record
            db.session.add(new_definition)  # Add the new definition to the database session
            db.session.commit()  # Commit the transaction to the database

            # Update the user's activity with the entered definition and action type
            user_activity = UserDefinitions.query.filter_by(profile_id=current_user.id, profile_definition=profile_game.random_definition).first()
            if user_activity is None:
                user_activity = UserDefinitions(
                    profile_id=current_user.id,
                    profile_definition=profile_game.random_definition,
                    action_type="entered",
                    revised_definition=entered_definition
                )
                db.session.add(user_activity)
                db.session.commit()
            else:
                user_activity.revised_definition = entered_definition
                user_activity.action_type = "entered"
                db.session.commit()

        ## no necesary    # Update the user's activity with the entered definition and action type
        ## no necesary    extended_user_activity = ExtendedUserDefinitions.query.filter_by(profile_id=current_user.id,
        ## no necesary                                                    profile_definition=profile_game.random_definition).first()  # Retrieve the user's activity record
        ## no necesary    extended_user_activity.revised_definition = entered_definition # Update the user's revised definition
        ## no necesary    extended_user_activity.action_type = "entered" # Update the user's activity type
        ## no necesary    db.session.commit()  # Commit the transaction to the database

            for owl_class in classes:
                if owl_class.name == random_word:

                    owl_class.comment.append(entered_definition) # Add the entered definition as a comment to the ontology class

            onto.save(file=ontology_path, format="rdfxml") # Save the updates to the ontology

        elif closest_definition: # Handle the user's closest definition selection
            # Decrease the score for the current high scored definition
            decrease_score_for_definition(profile_game.random_word, profile_game.random_definition, closest_definition)

            # Update the user's activity with the selected closest definition and action type
            user_activity = UserDefinitions.query.filter_by(profile_id=current_user.id,
                                                            profile_definition=profile_game.random_definition).first() # Retrieve the user's activity record
            user_activity.revised_definition = closest_definition # Update the user's revised definition
            user_activity.action_type = "selected" # Update the user's activity type
            db.session.commit()  # Commit the transaction to the database

            new_definition = DefinitionScores.query.filter_by(definition=closest_definition).first() # Retrieve the details for the selected closest definition
            increase_score_for_definition(new_definition.class_name, new_definition.definition) # Increase the score for the selected closest definition

        if question_number == profile_game.num_questions:
            # Redirect to the summary page if it's the last question
            return redirect(url_for('views.summary'))

        # Redirect to the next question
        return redirect(url_for('views.handle_question', question_number=next_question_number))

    return render_template('enter-definition.html', user=current_user, question_number=question_number)


@views.route('/find-closest-definition', methods=['POST'])
def find_closest_definition():
    """
    Find the closest definition to the entered definition and return the closest definition along with its semantic similarity score.

    Returns:
    JSON response containing the closest definition and its semantic similarity score.
    """
    entered_definition = request.json['enteredDefinition'] # Retrieve the entered definition from the JSON request

    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first() # Retrieve the user's game information

    closest_definition = find_closest_def(entered_definition, profile_game) # Find the closest definition to the entered definition

    # Return an empty string if no closest definition is found or if the closest definition is "No definition available"
    if not closest_definition or closest_definition == "No definition available":
        return jsonify({'closestDefinition': ""})

    # Return the closest definition in a JSON response
    return jsonify({'closestDefinition': closest_definition})

def calculate_vocabulary_enrichment_score(user_id, total_questions_played):
    """
    Calculate the vocabulary enrichment score based on the user's interactions in the game.

    Args:
    user_id: The user's identifier.
    total_questions_played: The total number of questions played by the user.

    Returns:
    The calculated vocabulary enrichment score on a 0-100 scale.
    """
    # Count the different types of user interactions
    user_agreements = UserDefinitions.query.filter_by(profile_id=user_id, action_type="agree").count()
    user_alternative_selections = UserDefinitions.query.filter_by(profile_id=user_id, action_type="selected").count()
    user_entered_selections = UserDefinitions.query.filter_by(profile_id=user_id, action_type="entered").count()
    user_pass_definitions = UserDefinitions.query.filter_by(profile_id=user_id, action_type="pass").count()

    # Normalize the user interactions to reflect their impact on the vocabulary enrichment
    normalized_user_agreements = user_agreements / total_questions_played
    normalized_user_alternative_selections = user_alternative_selections / total_questions_played
    normalized_user_pass_definitions = user_pass_definitions / total_questions_played
    normalized_user_entered = user_entered_selections / total_questions_played

    # Apply appropriate weightings to each type of interaction to reflect its impact on the vocabulary enrichment
    weighted_user_agreements = normalized_user_agreements * 35
    weighted_user_alternative_selections = normalized_user_alternative_selections * 30
    weighted_user_entered = normalized_user_entered * 25
    weighted_user_pass_definitions = normalized_user_pass_definitions * 10

    # Calculate the total vocabulary enrichment score on a 0-100 scale
    total_score = (weighted_user_agreements + weighted_user_alternative_selections + weighted_user_entered + weighted_user_pass_definitions)*2.5

    # Return the rounded total vocabulary enrichment score
    return round(total_score)



@views.route('/game/summary', methods=['GET', 'POST'])
@login_required
def summary():
    """
        Renders the summary page of the game.

        This function retrieves and calculates the necessary game information and user statistics for the summary page, ensuring that the current user is authenticated.

        Args:
        - None

        Returns:
        - Rendered template for the summary page with relevant game and user statistics
    """
    # Retrieve the user's game information and total number of questions
    profile_game = GameInformation.query.filter_by(profile_id=current_user.id).first()
    total_question = profile_game.num_questions

    # Calculate the XP, level progression, and vocabulary score for the user
    user_profile = Profile.query.filter_by(id=current_user.id).first()
    baseXP = 20
    performanceMultiplier = total_question/5
    vocab_score = calculate_vocabulary_enrichment_score(current_user.id, total_question)
    totalXP = baseXP  + performanceMultiplier * (1 + vocab_score/25)
    user_profile.xp += round(totalXP)
    db.session.commit()
    user_profile.level = level_progression(user_profile.xp)
    db.session.commit()

    # Retrieve user-defined definitions and their counts
    user_validated_definition = UserDefinitions.query.filter_by(profile_id=current_user.id, action_type="agree")
    user_revised_definition = UserDefinitions.query.filter(UserDefinitions.profile_id == current_user.id,or_(UserDefinitions.action_type == "selected",UserDefinitions.action_type == "entered"))
    user_passed_definition = UserDefinitions.query.filter_by(profile_id=current_user.id, action_type="pass")

    number_validated = user_validated_definition.count()
    number_revised = user_revised_definition.count()

    return render_template('summary.html', user=current_user, user_validated_definition=user_validated_definition,
                           user_revised_definition=user_revised_definition,
                           user_passed_definition=user_passed_definition, vocab_score=vocab_score, number_validated=number_validated, number_revised=number_revised, total_question=total_question)

@views.route('/game/detailed-overview', methods=['GET', 'POST'])
@login_required
def detailed_overview():
    """
       Renders a detailed game recap for the user.

       This function retrieves and calculates detailed game statistics, including user-defined definitions, validation, revision, and pass counts, and ensures that the current user is authenticated.

       Args:
       - None

       Returns:
       - Rendered template for the detailed overview with relevant game statistics and user-defined definitions
    """

    # Retrieve all user-engaged definitions and their related information
    all_user_definitions= UserDefinitions.query.filter_by(profile_id=current_user.id)
    definition_information =  [DefinitionScores.query.filter_by(class_name=definition.profile_class) for definition in all_user_definitions]

    # Retrieve user-engaged definitions and their types, and calculate counts
    user_validated_definition = UserDefinitions.query.filter_by(profile_id=current_user.id, action_type="agree")
    user_revised_definition = UserDefinitions.query.filter(UserDefinitions.profile_id == current_user.id,
                                                           or_(UserDefinitions.action_type == "selected",
                                                               UserDefinitions.action_type == "entered"))
    user_passed_definition = UserDefinitions.query.filter_by(profile_id=current_user.id, action_type="pass")

    validated_definition = [definition.profile_definition for definition in user_validated_definition]
    revised_definition = [definition.profile_definition for definition in user_revised_definition]
    passed_definition = [definition.profile_definition for definition in user_passed_definition]
    number_validated = user_validated_definition.count()
    number_revised = user_revised_definition.count()
    number_passed = user_passed_definition.count()
    return render_template('detailed-overview.html', user=current_user, user_validated_definition=validated_definition,
                           user_revised_definition=revised_definition,
                           user_passed_definition=passed_definition, number_validated=number_validated, number_revised=number_revised, number_passed=number_passed, definition_information=definition_information)



def level_progression(xp):
    """
    Calculate the level based on the accumulated experience points (xp) and the experience points required to reach the next level.

    Args:
    xp: The total accumulated experience points.

    Returns:
    The calculated level based on the experience points.
    """
    level = 0 # Initialize the level
    xp_to_reach_next_level = 0 # Initialize the experience points required to reach the next level

    # Calculate the level based on the accumulated experience points and the experience points required to reach the next level
    while xp_to_reach_next_level <= xp:
        level += 1 # Increment the level
        xp_to_reach_next_level += (level * 100) # Calculate the experience points required to reach the next level

    return level - 1 # Return the calculated level minus 1 (to adjust for the last level reached)
