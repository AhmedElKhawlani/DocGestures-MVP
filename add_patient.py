#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sqlite3 as sql
from alert import alert


def add_patient_to_db():
    db = sql.connect('data/data.db')
    cur = db.cursor()
    try:
        last_name = entry_last_name.get().upper()
        first_name = entry_first_name.get().capitalize()
        sex = combo_sex.get()
        birth_year = int(entry_birth_year.get())

        cur.execute('''INSERT INTO Patients (Last_Name, First_Name, Gender,
                      Year_of_Birth) VALUES (?, ?, ?, ?)''',
                    (last_name, first_name, sex, birth_year))
        db.commit()
        ajouter_patient.destroy()
        alert("Success", "Patient added successfully")
    except Exception as e:
        alert("Error", f"Error: {str(e)}, patient not added")
    finally:
        db.close()


def show_add_patient_window():
    global ajouter_patient, entry_last_name, entry_first_name
    global combo_sex, entry_birth_year
    ajouter_patient = Tk()
    ajouter_patient.title("DOC GESTURES - Add Patient")
    ajouter_patient.resizable(width=False, height=False)

    # Labels
    label_last_name = Label(ajouter_patient, text="Last Name")
    label_first_name = Label(ajouter_patient, text="First Name")
    label_sex = Label(ajouter_patient, text="Sex")
    label_birth_year = Label(ajouter_patient, text="Year of Birth")

    # Input fields
    entry_last_name = Entry(ajouter_patient)
    entry_first_name = Entry(ajouter_patient)
    combo_sex = ttk.Combobox(ajouter_patient)
    entry_birth_year = Entry(ajouter_patient)
    button_add = Button(ajouter_patient, text="Add to the database",
                        command=add_patient_to_db)

    # Grid layout
    label_last_name.grid(column=1, row=1, padx=10, pady=10, columnspan=5)
    label_first_name.grid(column=1, row=3, padx=10, pady=10, columnspan=5)
    label_sex.grid(column=1, row=5, padx=10, pady=10, columnspan=5)
    label_birth_year.grid(column=1, row=7, padx=10, pady=10, columnspan=5)

    entry_last_name.grid(column=6, row=1, padx=10, pady=10, columnspan=4)
    entry_first_name.grid(column=6, row=3, padx=10, pady=10, columnspan=4)
    combo_sex.grid(column=6, row=5, padx=10, pady=10, columnspan=4)
    entry_birth_year.grid(column=6, row=7, padx=10, pady=10, columnspan=4)
    button_add.grid(column=3, row=9, padx=10, pady=10, columnspan=6)

    # Combo box values for sex
    combo_sex['values'] = ["Male", "Female", "Other"]

    # Layout adjustments
    label_adjust1 = Label(ajouter_patient, text=" ")
    label_adjust2 = Label(ajouter_patient, text=" ")

    label_adjust1.grid(column=0, row=1, padx=10, pady=10, columnspan=3)
    label_adjust2.grid(column=11, row=1, padx=10, pady=10, columnspan=3)

    ajouter_patient.mainloop()
