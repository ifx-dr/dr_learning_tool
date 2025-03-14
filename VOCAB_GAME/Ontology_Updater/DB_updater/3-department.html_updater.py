import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to the database
conn = sqlite3.connect("C:\\Users\\UribelarreaJ\\Desktop\\OntoQuest-main\\VOCAB_GAME\\FLASK\\website\\database.db")
cursor = conn.cursor()

# Get the list of departments from the database
cursor.execute("SELECT department FROM department_ontology_association")
departments = list(set([row[0] for row in cursor.fetchall()]))

# Read the existing HTML file
with open("C:\\Users\\UribelarreaJ\\Desktop\\OntoQuest-main\\VOCAB_GAME\\FLASK\\website\\templates\\department.html", "r") as f:
    html = f.read()

# Extract the existing departments from the HTML file
existing_departments = []
start_index = html.find("<select name=\"departments\" id=\"department-select\" autocomplete=\"on\">")
end_index = html.find("</select>")
for line in html[start_index:end_index].split("\n"):
    if "<option" in line:
        existing_departments.append(line.split(">")[1].split("<")[0])

# Create a list of new departments to add
new_departments = [department for department in departments if department not in existing_departments]

# Create a list of departments to remove
departments_to_remove = [department for department in existing_departments if department not in departments and department != "--Please choose an option--"]

# Create a Tkinter window for the pop-up
root = tk.Tk()
root.withdraw()  # Hide the window

# Create a pop-up window to show the departments
popup = tk.Toplevel(root)
popup.title("Departments Updated")
popup_label = tk.Label(popup, text="Departments updated:")
popup_label.pack()
department_list = tk.Listbox(popup)
department_list.pack()
for department in new_departments:
    department_list.insert(tk.END, f"Added: {department}")
for department in departments_to_remove:
    department_list.insert(tk.END, f"Removed: {department}")
popup_button = tk.Button(popup, text="OK", command=popup.destroy)
popup_button.pack()

# Wait for the user to close the pop-up
popup.wait_window(popup)

# Update the HTML file
with open("C:\\Users\\UribelarreaJ\\Desktop\\OntoQuest-main\\VOCAB_GAME\\FLASK\\website\\templates\\department.html", "w") as f:
    html_lines = html.split("\n")
    new_html_lines = []
    for line in html_lines:
        if "<option" in line:
            department = line.split(">")[1].split("<")[0]
            if department in departments or department == "--Please choose an option--":
                new_html_lines.append(line)
        else:
            new_html_lines.append(line)
    html = "\n".join(new_html_lines)
    f.write(html)

# Close the database connection
conn.close()
