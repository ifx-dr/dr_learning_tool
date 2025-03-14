FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Download the NLTK package
RUN python -c "import nltk; nltk.download('punkt')"

# Copy the folder VOCAB_GAME
COPY VOCAB_GAME .

# Set the working directory in the FLASK folder
WORKDIR /app/VOCAB_GAME/FLASK

# Copy the app.py file
COPY VOCAB_GAME/FLASK .

# Set environment variables

# Set the environment variable for the Flask application
ENV FLASK_APP=app.py

# Execute the command to start the Gunicorn application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--timeout", "300"]