import os
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Set the directory path and database path
directory_path = "C:\\Users\\UribelarreaJ\\Desktop\\OntoQuest\\VOCAB_GAME\\FLASK\\website\\static\\ontologies"
database_path = "C:\\Users\\UribelarreaJ\\Desktop\\OntoQuest\\VOCAB_GAME\\FLASK\\website\\database.db"

# Connect to the database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Create the ontology meta table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ontology (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        image_url TEXT,
        ontology_url TEXT
    )
""")

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    # Check if the file has an .rdf extension
    if filename.endswith('.rdf'):
        # Get the file name without extension
        file_name = os.path.splitext(filename)[0]
        
        # Create a nice name for the ontology
        nice_name = file_name.replace('_', ' ').title()
        
        # Create the image URL
        image_url = f"picture/ontologies_pictures/{file_name}.jpg"
        
        # Check if the ontology already exists in the database
        cursor.execute("SELECT * FROM ontology WHERE name = ?", (nice_name,))
        if cursor.fetchone() is None:
            # Create a Tkinter window for the pop-up
            root = tk.Tk()
            root.withdraw()  # Hide the window
            
            # Create a pop-up window to ask for description
            popup = tk.Toplevel(root)
            popup.title("Add Ontology")
            popup_label = tk.Label(popup, text=f"Add ontology: {nice_name}")
            popup_label.pack()
            description_entry = tk.Text(popup, height=5, width=40)
            description_entry.pack()
            def add_ontology():
                description = description_entry.get("1.0", "end-1c")
                if description:
                    cursor.execute("""
                        INSERT INTO ontology (name, description, image_url, ontology_url)
                        VALUES (?, ?, ?, ?)
                    """, (nice_name, description, image_url, filename))
                    conn.commit()
                else:
                    cursor.execute("""
                        INSERT INTO ontology (name, description, image_url, ontology_url)
                        VALUES (?, ?, ?, ?)
                    """, (nice_name, "", image_url, filename))
                    conn.commit()
                popup.destroy()
            def skip():
                cursor.execute("""
                    INSERT INTO ontology (name, description, image_url, ontology_url)
                    VALUES (?, ?, ?, ?)
                """, (nice_name, "", image_url, filename))
                conn.commit()
                popup.destroy()
            add_button = tk.Button(popup, text="Add", command=add_ontology)
            add_button.pack()
            skip_button = tk.Button(popup, text="Skip", command=skip)
            skip_button.pack()
            
            # Wait for the user to close the pop-up
            popup.wait_window(popup)

# Close the database connection
conn.close()
