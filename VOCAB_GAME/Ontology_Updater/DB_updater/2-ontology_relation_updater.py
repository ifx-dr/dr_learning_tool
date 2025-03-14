import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to the database
conn = sqlite3.connect("C:\\Users\\UribelarreaJ\\Desktop\\OntoQuest-main\\VOCAB_GAME\\FLASK\\website\\database.db")
cursor = conn.cursor()

# Create a Tkinter window for the pop-ups
root = tk.Tk()
root.withdraw()  # Hide the window

# Get the list of departments from the database
cursor.execute("SELECT department FROM department_ontology_association")
departments = list(set([row[0] for row in cursor.fetchall()]))

# Create a pop-up window to select the department
department_popup = tk.Toplevel(root)
department_popup.title("Select Department")
department_label = tk.Label(department_popup, text="Select a department:")
department_label.pack()
department_var = tk.StringVar()
department_menu = ttk.Combobox(department_popup, textvariable=department_var)
department_menu['values'] = departments + ["Add new department"]
department_menu.pack()
department_button = tk.Button(department_popup, text="Select", command=department_popup.destroy)
department_button.pack()

# Wait for the user to select a department
department_popup.wait_window(department_popup)
department = department_var.get()

if department == "Add new department":
    # Create a new pop-up window to enter the new department name
    new_department_popup = tk.Toplevel(root)
    new_department_popup.title("Enter New Department")
    new_department_label = tk.Label(new_department_popup, text="Enter the new department name:")
    new_department_label.pack()
    new_department_entry = tk.Entry(new_department_popup)
    new_department_entry.pack()
    new_department_button = tk.Button(new_department_popup, text="Add", command=new_department_popup.destroy)
    new_department_button.pack()
    new_department_popup.wait_window(new_department_popup)
    department = new_department_entry.get()

# Get the list of ontologies from the database
cursor.execute("SELECT name FROM ontology")
ontologies = [row[0] for row in cursor.fetchall()]

# Create a pop-up window to select the ontologies
ontology_popup = tk.Toplevel(root)
ontology_popup.title("Select Ontologies")
ontology_label = tk.Label(ontology_popup, text="Select one or more ontologies:")
ontology_label.pack()
ontology_vars = []
for ontology in ontologies:
    var = tk.IntVar()
    checkbox = tk.Checkbutton(ontology_popup, text=ontology, variable=var)
    checkbox.pack()
    ontology_vars.append(var)
ontology_button = tk.Button(ontology_popup, text="Select", command=ontology_popup.destroy)
ontology_button.pack()

# Wait for the user to select the ontologies
ontology_popup.wait_window(ontology_popup)
selected_ontologies = [ontology for i, ontology in enumerate(ontologies) if ontology_vars[i].get()]

# Update the department_ontology_association table
for ontology in selected_ontologies:
    cursor.execute("SELECT id FROM ontology WHERE name = ?", (ontology,))
    ontology_id = cursor.fetchone()[0]
    cursor.execute("INSERT OR IGNORE INTO department_ontology_association (department, ontology_id) VALUES (?, ?)", (department, ontology_id))
    conn.commit()

# Close the database connection
conn.close()
