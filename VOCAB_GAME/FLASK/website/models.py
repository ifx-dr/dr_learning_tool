from . import db
from flask_login import UserMixin
import owlready2

# Define the User model for storing user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the user
    email = db.Column(db.String(150), unique=True, nullable=False)  # User's email address
    password = db.Column(db.String(150), nullable=False)  # User's password
    first_name = db.Column(db.String(150), nullable=False)  # User's first name
    profile = db.relationship('Profile', uselist=False, back_populates="user")

# Define the Profile model for storing user profiles
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the profile
    username = db.Column(db.String(150), nullable=False)  # User's username
    profile_picture = db.Column(db.String(150))  # File path for the profile picture
    level = db.Column(db.Integer)  # User's level in the game
    xp = db.Column(db.Integer, default=0)  # User's experience points, default to 0
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key reference to the associated User
    user = db.relationship('User', back_populates="profile")

# Define the Ontology model for storing ontology information
class Ontology(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the ontology
    name = db.Column(db.String(150), nullable=False)  # Name of the ontology, required
    description = db.Column(db.String(1000))  # Description of the ontology
    image_url = db.Column(db.String(255))  # URL to the image associated with the ontology
    ontology_url = db.Column(db.String(255))  # URL to the ontology resource

# Define the DepartmentOntologyAssociation model for associating departments with ontologies
class DepartmentOntologyAssociation(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the association
    department = db.Column(db.String(150), nullable=False)  # Name of the department, required
    ontology_id = db.Column(db.Integer, db.ForeignKey('ontology.id'), nullable=False)  # Foreign key reference to the associated Ontology
    ontology = db.relationship('Ontology', backref='department_associations')  # Define the relationship with the Ontology model

# Define the GameInformation model for storing game-related information
class GameInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the game information
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)  # Foreign key reference to the associated Profile
    department = db.Column(db.String(150))  # Department related to the game information
    ontology_id = db.Column(db.Integer, db.ForeignKey('ontology.id'))  # Foreign key reference to the associated Ontology
    num_questions = db.Column(db.Integer)  # Number of questions in the game
    random_word = db.Column(db.String(150))  # Randomly current selected word for the game
    random_definition = db.Column(db.String(1000))  # Random current definition associated with the word

    profile = db.relationship('Profile', backref='game_information')  # Define the relationship with the Profile model
    ontology = db.relationship('Ontology', backref='game_information')  # Define the relationship with the Ontology model

# Define the UsedWord model for storing information about words used in the game
class UsedWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the used word
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)  # Foreign key reference to the associated Profile
    word_uri = db.Column(db.String)  # URI of the used word

    profile = db.relationship('Profile', backref='used_word')  # Define the relationship with the Profile model

    def get_word(self, ontology_path):
        """
        Get the word from the ontology using its URI
        :param ontology_path: Path to the ontology file
        :return: The word from the ontology
        """
        return owlready2.get_ontology("file://" + ontology_path).search_one(iri=self.word_uri)

# Define the DefinitionScores model for storing scores and information related to definitions
class DefinitionScores(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the definition score
    class_name = db.Column(db.String(150))  # Name of the class or entity associated with the definition
    definition = db.Column(db.String(1000))  # The definition text
    score = db.Column(db.Float, default=0)  # Score associated with the definition
    agreements = db.Column(db.Integer, default=0)  # Number of agreements on the definition
    disagreements = db.Column(db.Integer, default=0)  # Number of disagreements on the definition
    latest_review = db.Column(db.Integer, default=0)  # Timestamp of the latest review
    split_review = db.Column(db.Boolean, default=False)  # Indicates whether the review is split
    is_default = db.Column(db.Boolean, default=False)  # Indicates the absence of a current definition

# Define the UserDefinitions model for storing user-related definitions and actions
class UserDefinitions(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the user definition
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id',ondelete='CASCADE'), nullable=False)  # Foreign key reference to the associated Profile
    profile_class = db.Column(db.String(150), db.ForeignKey('definition_scores.class_name', ondelete='CASCADE'))  # Class name associated with the definition score
    profile_definition = db.Column(db.String(1000), db.ForeignKey('definition_scores.definition', ondelete='CASCADE'))  # Definition associated with the definition score
    action_type = db.Column(db.String(50))  # Type of action performed (agree, pass, selection of alternative, entered definition)
    revised_definition = db.Column(db.String(1000), db.ForeignKey('definition_scores.definition', ondelete='CASCADE'))  # Revised definition associated with the definition score

    profile = db.relationship('Profile', backref='user_definitions')  # Define the relationship with the Profile model
    profile_definition_ref = db.relationship('DefinitionScores', foreign_keys=[profile_definition], backref='user_definitions_profile')  # Define the relationship with the original profile definition
    revised_definition_ref = db.relationship('DefinitionScores', foreign_keys=[revised_definition], backref='user_definitions_revised')  # Define the relationship with the revised definition
    profile_class_ref = db.relationship('DefinitionScores', foreign_keys=[profile_class], backref='user_definitions_class')  # Define the relationship with the profile class

# Define the extended UserDefinitions model, with the data from Additional information
class ExtendedUserDefinitions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile_class = db.Column(db.String(150), db.ForeignKey('definition_scores.class_name'))
    profile_definition = db.Column(db.String(1000), db.ForeignKey('definition_scores.definition'))
    action_type = db.Column(db.String(50))
    revised_definition = db.Column(db.String(1000), db.ForeignKey('definition_scores.definition'))
    alternative_name = db.Column(db.String(100))
    abbreviation = db.Column(db.String(100))
    #german_name = db.Column(db.String(100))
    example = db.Column(db.String(1000))
    ontology_iri = db.Column(db.String(250))

    profile = db.relationship('Profile', backref='extended_user_definitions')
    profile_definition_ref = db.relationship('DefinitionScores', foreign_keys=[profile_definition], backref='extended_user_definitions_profile')
    revised_definition_ref = db.relationship('DefinitionScores', foreign_keys=[revised_definition], backref='extended_user_definitions_revised')
    profile_class_ref = db.relationship('DefinitionScores', foreign_keys=[profile_class], backref='extended_user_definitions_class')


# Define the Challenges model for storing game challenges and associated XP rewards
class Challenges(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the challenge
    challenge = db.Column(db.String(1000))  # Description of the challenge
    xp_reward = db.Column(db.Integer, default=0)  # XP reward for completing the challenge
    name = db.Column(db.String(1000))

# Define the UserChallenges model for associating users with challenges and their completion status
class UserChallenges(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the user's challenge association
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key reference to the associated User
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)  # Foreign key reference to the associated Challenge
    completed = db.Column(db.Boolean, default=False)  # Indicates if the challenge has been completed or not

    user = db.relationship('User', backref='user_challenges')  # Define the relationship with the User model
    challenge = db.relationship('Challenges', backref='user_association')  # Define the relationship with the Challenge model

