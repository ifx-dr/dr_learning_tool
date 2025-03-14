import sqlite3
import tkinter as tk
from tkinter import messagebox

# Set the database path
database_path = "C:\\Users\\UribelarreaJ\\Desktop\\OntoQuest-main\\VOCAB_GAME\\FLASK\\website\\database.db"

# Connect to the database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Get all ontologies with empty descriptions
cursor.execute("SELECT * FROM ontology WHERE description = ''")
ontologies = cursor.fetchall()

# Loop through each ontology
for ontology in ontologies:
    # Get the name of the ontology
    name = ontology[1]
    
    # Create a Tkinter window for the pop-up
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create a pop-up window to ask for description
    popup = tk.Toplevel(root)
    popup.title("Add Description")
    popup_label = tk.Label(popup, text=f"Add description for: {name}")
    popup_label.pack()
    description_entry = tk.Text(popup, height=5, width=40)
    description_entry.pack()
    def update_description():
        description = description_entry.get("1.0", "end-1c")
        if description:
            cursor.execute("UPDATE ontology SET description = ? WHERE name = ?", (description, name))
            conn.commit()
        popup.destroy()
    add_button = tk.Button(popup, text="Add", command=update_description)
    add_button.pack()
    
    # Wait for the user to close the pop-up
    popup.wait_window(popup)

# Close the database connection
conn.close()
