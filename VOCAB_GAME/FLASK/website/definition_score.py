import nltk
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from flask import flash
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from . import db
from .models import DefinitionScores
import time


#nltk.download('punkt', force=True)
nltk.download('punkt', force=False)
nltk.download('punkt_tab')

def get_highest_scored_definition(random_word):
    """
    Retrieve the definition with the highest score for the random word's class.

    Args:
    random_word: The random word for which the definition is to be retrieved.

    Returns:
    The definition with the highest score for the random word's class.
    """
    # Logic to retrieve the definition with the highest score for the random word's class
    #highest_scored_definition = DefinitionScores.query.filter_by(class_name=random_word.name).order_by(DefinitionScores.score.desc()).first()
    #highest_scored_definition = DefinitionScores.query.filter_by(class_name=random_word.name).first()

    #if highest_scored_definition:
    #    return highest_scored_definition.definition
    #else:
    #    flash('No definition for this term', category='error')  # Handle potential exceptions that could occur during the retrieval process
    
    definition = "No definition available"    
    if random_word.comment:
        definition = str(random_word.comment[0])
    elif random_word.label:
        definition = str(random_word.label[0])
        
    return definition

def increase_score_for_definition(random_word, definition):
    """
    Increase the score for the specific definition and update the agreements count.

    Args:
    random_word: The random word for which the score is to be increased.
    definition: The specific definition for which the score is to be increased.
    """
    # Logic to increase the score for the specific definition
    definition_score = DefinitionScores.query.filter_by(class_name=random_word, definition=definition).first()
    if definition_score: # Check if the definition score exists
        # Calculate weighted increment based on the number of previous agreements and community consensus
        weighted_increment = 1 + (0.1 * definition_score.agreements)
        definition_score.score += weighted_increment  # Increase the score
        definition_score.agreements += 1  # Increment the agreements count
    else:
        # Add a new record with a score of 1
        new_definition_score = DefinitionScores(class_name=random_word, definition=definition, score=1, agreements=1)
        db.session.add(new_definition_score)

    perform_stability_check(definition_score) # Perform a stability check
    db.session.commit()  # Commit the changes to the database


def decrease_score_for_definition(random_word, disagree_definition, agree_definition):
    """
    Decrease the score for the specific definition and update the disagreements count.

    Args:
    random_word: The random word for which the score is to be decreased.
    disagree_definition: The specific definition for which the score is to be decreased.
    agree_definition: The definition with which disagreement occurred.
    """
    # Logic to decrease the score for the specific definition
    definition_score = DefinitionScores.query.filter_by(class_name=random_word, definition=disagree_definition).first()
    semantic_score = semantic_similarity(disagree_definition, agree_definition)
    weighted_decrement = calculate_weighted_decrement(definition_score, semantic_score)
    if definition_score and definition_score.score > 0: # Check if the definition score exists and if the current definition score is positive
        definition_score.disagreements += 1  # Increment the disagreements count
        future_score = definition_score.score - weighted_decrement
        if future_score >= 0: # Check if the future score is still going to be positive or null
            definition_score.score -= weighted_decrement  # Decrease the score
        else:
            definition_score.score = 0 # Set the score to 0 if future score becomes negative

    perform_stability_check(definition_score) # Perform a stability check
    db.session.commit() # Commit the changes to the database

def calculate_weighted_decrement(definition_score, semantic_score):
    """
    Calculate the weighted decrement based on the semantic difference.

    Args:
    definition_score: The score of the specific definition.
    semantic_score: The semantic difference score.

    Returns:
    The calculated weighted decrement.
    """
    # Logic to calculate weighted decrement based on the semantic difference
    default_decrement = 1  # Default decrement for user disagreement

    if definition_score:
        # Apply weighted decrement based on the semantic difference
        weighted_decrement = 1 + (1 - semantic_score)
        if semantic_score < 0.2:  # Increase the decrement for significant semantic differences
            weighted_decrement *= 1.7
        elif semantic_score < 0.5:  # Moderately significant semantic differences
            weighted_decrement *= 1.5
        else:  # Relatively minor semantic differences
            weighted_decrement *= 1.3
        weighted_decrement = round(weighted_decrement, 3)  # Round the weighted decrement to three decimal places

        return weighted_decrement
    else:
        return default_decrement  # Return the default decrement for user disagreement if the definition score is not available

def semantic_similarity(definition1, definition2):
    """
    Calculate the semantic similarity score between two definitions using Doc2Vec model.

    Args:
    definition1: The first definition for semantic comparison.
    definition2: The second definition for semantic comparison.

    Returns:
    The semantic similarity score between the two definitions.
    """
    data = [definition2] # Prepare the second definition for comparison
    semantic_score = 0  # Initialize the semantic score

    tokenized_data = [word_tokenize(document.lower()) for document in data] # Tokenize the data (convert text into tokens)

    # Creating TaggedDocument objects for training
    tagged_data = [TaggedDocument(words=words, tags=[str(idx)]) for idx, words in enumerate(tokenized_data)]

    # Initialize and train the Doc2Vec model
    model = Doc2Vec(vector_size=100, window=3, min_count=1, workers=4, epochs=1000)
    model.build_vocab(tagged_data) # Build vocabulary
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs) # Train the model

    # Infer vector for the new document (definition1)
    new_data = definition1
    inferred_vector = model.infer_vector(word_tokenize(new_data.lower())) # Infer the vector for the new definition

    # Find the most similar documents based on the inferred vector
    similar_documents = model.dv.most_similar([inferred_vector], topn=len(model.dv))

    # Calculate the semantic similarity score based on the most similar document
    for index, score in similar_documents:
        semantic_score = score  # Assign the score from the most similar document

    return semantic_score # Return the calculated semantic similarity score

def perform_stability_check(definition):
    """
    Perform a stability check on the definition based on the number of reviews and the frequency of the check.

    Args:
    definition: The definition for which the stability check is to be performed.
    """
    current_number_review = definition.agreements + definition.disagreements # Calculate the current number of reviews

    if current_number_review > 20: # Check if the number of reviews exceeds the minimum threshold
        review_frequency = 10*(current_number_review // 20) # Calculate the review frequency based on the number of reviews

        if current_number_review - definition.latest_review >= review_frequency:  # Perform stability check based on review frequency
            definition.latest_review = current_number_review # Update the latest review count
            check_threshold_stability(definition) #Perform the stability threshold check


def adjust_instability_threshold(total_reviews, current_threshold):
    """
    Dynamically adjust the instability interval boundaries based on the total number of reviews.

    Args:
    total_reviews: The total number of reviews.
    current_threshold: The current stability threshold boundaries as a tuple.

    Returns:
    The adjusted stability threshold boundaries as a tuple.
    """
    lower_bound = current_threshold[0] + (total_reviews * 0.005)  # Increase lower bound with increasing reviews
    upper_bound = current_threshold[1] - (total_reviews * 0.005)  # Decrease upper bound with increasing reviews

    if upper_bound < lower_bound: # Ensure upper bound does not fall below the lower bound
        upper_bound = lower_bound  # Set upper bound equal to lower bound to avoid overlap

    return (max(0.40,lower_bound), min(0.60,upper_bound))  # Return the adjusted stability threshold boundaries as a tuple
def check_threshold_stability(definition):
    """
    Evaluate the stability of a definition based on the ratio of agreements to total reviews and manage it accordingly.

    Args:
    definition: The definition to be evaluated for stability.

    Returns:
    True if the definition is marked for split review, otherwise False.
    """
    agreements = definition.agreements
    disagreements = definition.disagreements
    total_reviews = agreements + disagreements

    stability_threshold = (0.45, 0.55) # Threshold boundaries for stability evaluation
    invalid_threshold = 0.1 # Threshold for identifying invalid definitions

    current_stability_threshold = adjust_instability_threshold(total_reviews, stability_threshold) # Adjust the instability threshold based on the total number of reviews

    ratio = agreements / total_reviews # Calculate the ratio of agreements to total reviews

    if ratio >= current_stability_threshold[0] and ratio <= current_stability_threshold[1]: # Mark the definition for split review if it is not stable,it means there is too much contradiction (equivalent number of agreements/disagreements)
        return split_definition(definition.class_name)

    elif ratio < invalid_threshold:   # Delete the definition if it is not valid due to too many disagreements
        db.session.delete(definition)
        db.session.commit()


def vectorize_definitions(definitions):
    """
    Vectorize the definitions based on semantic similarity.

    Args:
    definitions: The list of definitions to be vectorized.

    Returns:
    A 2D array of vectorized definitions based on semantic similarity.
    """

    vectorized_definitions = []  # Initialize the list for vectorized representations

    for definition in definitions:
        semantic_vector = []  # Initialize the semantic vector for the current definition

        for other_definition in definitions:
            # Calculate the semantic similarity score between the current and other definitions
            similarity_score = semantic_similarity(definition, other_definition)
            semantic_vector.append(similarity_score) #Append the similarity score to the semantic vector
        vectorized_definitions.append(semantic_vector) #Append the semantic vector to the list of vectorized definitions

    return np.array(vectorized_definitions) # Return the vectorized definitions as a 2D numpy array

def create_cluster_definitions(definitions):
    """
    Perform hierarchical clustering on definitions based on semantic similarity.

    Args:
    class_name: The class name for which definitions are to be clustered.

    Returns:
    The cluster labels for the definitions.
    """

    vectorized_definitions = vectorize_definitions(definitions)  # Vectorize the definitions based on semantic similarity

    # Perform hierarchical clustering based on semantic similarity
    clustering_model = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    clusters = clustering_model.fit_predict(vectorized_definitions) # Fit the model and predict the clusters

    return clusters  # Return the cluster labels for the definitions

def check_number_definition(class_name):
    """
    Manage and consolidate definitions based on their numbers and perform clustering if needed.

    Args:
    class_name: The class name for which definitions are to be managed.

    Returns:
    None
    """
    definitions = DefinitionScores.query.filter_by(class_name=class_name).all() # Retrieve definitions for the specified class
    total_number_definitions = len(definitions)  #Calculate the total number of definitions

    if total_number_definitions > 10: # Condition for the clustering to be relevant
        split_definition(class_name)
        clusters = create_cluster_definitions(class_name)  # Perform clustering based on semantic similarity
        # Group definitions by clusters for further consolidation
        clustered_definitions = {}  # Dictionary to store definitions grouped by clusters
        for idx, cluster_id in enumerate(clusters):
            if cluster_id not in clustered_definitions:
                clustered_definitions[cluster_id] = []
            clustered_definitions[cluster_id].append(definitions[idx])

        for cluster_id, cluster_definitions in clustered_definitions.items():  # Consolidate definitions within each cluster
            if len(cluster_definitions) > 1:
                # Find the definition with the highest ratio of agreements
                max_agreement_ratio = 0
                selected_definition = None
                for definition in cluster_definitions:
                    agreement_ratio = definition.agreements / (definition.agreements + definition.disagreements)
                    if agreement_ratio > max_agreement_ratio:
                        max_agreement_ratio = agreement_ratio
                        selected_definition = definition

                # Regroup all definitions in the cluster to the selected definition
                for definition in cluster_definitions:
                    if definition != selected_definition:
                        db.session.delete(definition)  # Delete the redundant definition

        db.session.commit()

def split_definition(class_name):
    """
    Mark all definitions of a specific class for split review.

    Args:
    class_name: The class name for which definitions are to be marked for split review.

    Returns:
    True if the operation is successful, otherwise False.
    """
    definitions = DefinitionScores.query.filter_by(class_name=class_name).all() # Retrieve all definitions for the specified class

    for definition in definitions:
        definition.split_review = True # Mark each definition for split review

    return True # Return True to indicate successful completion


def find_closest_def(entered_definition, profile_game):
    """
    Find the closest definition to the entered definition for the current random word.

    Args:
    entered_definition: The user-entered definition.
    profile_game: The user's game information.

    Returns:
    The closest definition to the entered definition.
    """
    start_time = time.time() # Record the start time for performance measurement
    random_word = profile_game.random_word # Retrieve the current random word

    # Retrieve other definitions for the random word
    other_definitions = DefinitionScores.query.filter(DefinitionScores.class_name == random_word, DefinitionScores.definition != entered_definition)

    # Check if there are other definitions available and find the closest one based on semantic similarity
    if not other_definitions:
        print("--- %s seconds ---" % (time.time() - start_time)) # Print the elapsed time for performance measurement
        # Return None if no other definitions are available
        return None
    elif other_definitions.count() == 0: #Check that if the array legth is greater than 0. If not return None.
        return None
    elif other_definitions[0].definition == "No definition available":
        print("--- %s seconds ---" % (time.time() - start_time)) # Print the elapsed time for performance measurement
        # Return None if the first definition is "No definition available"
        return None

    closest_definition = None # Initialize the closest definition
    semantic_score = -1 # Initialize the semantic score

    for definition in other_definitions:
        # Calculate the semantic similarity and find the closest definition
        if semantic_similarity(entered_definition, definition.definition) > semantic_score:
            semantic_score = semantic_similarity(entered_definition, definition.definition)  # Update the semantic score
            closest_definition = definition.definition  # Update the closest definition
    print("--- %s seconds ---" % (time.time() - start_time))

    # Print the elapsed time for performance measurement
    return closest_definition  # Return the closest definition
#