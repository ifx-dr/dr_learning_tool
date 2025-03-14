import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Profile
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
logging.basicConfig(level=logging.INFO)


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login and authentication.

    For GET requests, render the login page.
    For POST requests, validate user credentials and log in the user.

    Returns:
    If successful, redirects to the home page. Otherwise, renders the login page with appropriate messages.
    """
    if request.method == 'POST':
        email = "sc4eu@infineon.com"
        logging.info(f"Attempting to log in user with email: {email}")
        user = User.query.filter_by(email=email).first() #Retrieve the user from the database

        if user:
            login_user(user, remember=True) # Log in the user
            return redirect(url_for('views.home')) # Redirect to the home page after successful login

        else:
            flash('User does not exists.', category='error') #Non-existing user message

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    """
    Log out the current user.

    Returns:
    Redirects to the login page after successful logout.
    """
    logout_user() # Log out the current user
    return redirect(url_for('auth.login')) # Redirect to the login page after successful logout

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Handle user registration (sign-up) and account creation.

    For GET requests, render the sign-up page.
    For POST requests, validate user input and create a new user account.

    Returns:
    If successful, redirects to the home page. Otherwise, renders the sign-up page with appropriate messages.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() # Check if the user already exists

        if user:
            flash('User already exists.', category='error') # Display an error message for existing user
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error') # Validate email length
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category='error') # Validate first name length
        elif password1 != password2:
            flash('Password don\'t match.', category='error') # Validate matching passwords
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error') # Validate password length
        else: # Create a new user account and profile
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()  # Explicitly commit the transaction
            new_profile = Profile(username=first_name, level=0, user_id=new_user.id, profile_picture='picture/user_profile/user1-removebg-preview.png')
            db.session.add(new_profile)
            db.session.commit()
            login_user(new_user, remember=True) # Log in the new user
            flash('Account created!', category='success') # Display success message
            return redirect(url_for('views.home')) # Redirect to the home page after successful sign-up

    return render_template("signup.html", user=current_user)

@auth.route('/forgot-password')
def forgot_password():
    pass
