#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import datetime

from alert import *
from get_data_from_widget import *

# *************************************************************************************************************
# ****************************************** function get_info ************************************************
# *************************************************************************************************************    

def get_info():
    global data
    BD = sql.connect('data/DOC HAJAR.db')
    cur = BD.cursor()
    patient = str(combo_patient.get())
    patient_id = patient.split()[0]
    
    # Fetch sex and birth year from database
    cur.execute("SELECT SEXE FROM Patients WHERE ID = ?", (patient_id,))
    sex = cur.fetchall()[0][0]
    
    cur.execute("SELECT ANNEE_NAISSANCE FROM Patients WHERE ID = ?", (patient_id,))
    birth_year = cur.fetchall()[0][0]
    
    # Calculate age
    today = datetime.date.today()
    age = today.year - birth_year

    # Update labels with fetched data
    label_sex = Label(controle2, text=sex)
    label_age = Label(controle2, text=str(age) + " years")
    label_sex.grid(column=15, row=1, padx=10, pady=10, columnspan=10)
    label_age.grid(column=20, row=1, padx=10, pady=10, columnspan=10)
    
    # Fetch last consultation details
    cur.execute(
        "SELECT * FROM Consultations WHERE ID_Patient = ? ORDER BY Date_Consultation DESC", (patient_id,)
    )
    
    try:
        data = cur.fetchall()[0]
        (
            date_consult, motif_consult, antecedent_consult, examens_consult, ordonance_consult, 
            bilan_consult, resultats, specialiste_consult, avis_specialiste, notes_controle1
        ) = data[2:12]

        label_date_consultation = Label(controle2, text="Last consultation date: " + date_consult)
        label_date_consultation.grid(column=20, row=2, padx=10, pady=10, columnspan=10)

        # Clear previous data in text fields
        for field in [
            entry_motif, entry_antecedent, entry_examen, entry_ordonnance, 
            entry_bilan, entry_resultat, entry_avisspe, entry_controle1
        ]:
            field.delete(0.0, END)
        entry_specialiste.delete(0, END)

        # Insert new data
        entry_motif.insert(0.0, motif_consult)
        entry_antecedent.insert(0.0, antecedent_consult)
        entry_examen.insert(0.0, examens_consult)
        entry_ordonnance.insert(0.0, ordonance_consult)
        entry_bilan.insert(0.0, bilan_consult)
        entry_resultat.insert(0.0, resultats)
        entry_specialiste.insert(0, specialiste_consult)
        entry_avisspe.insert(0.0, avis_specialiste)
        entry_controle1.insert(0.0, notes_controle1)
    
    except IndexError:
        alert("Error", "No consultations found for this patient")


# *************************************************************************************************************
# *********************************** Save consultation data to database **************************************
# ************************************************************************************************************* 

def save_record():
    try:
        BD = sql.connect('data/DOC HAJAR.db')
        cur = BD.cursor()
        patient_id = str(data[0])
        controle2_content = get_text_from_text_widget(entry_controle2, 0)

        cur.execute(
            "UPDATE Consultations SET Controle2 = ? WHERE ID = ?", 
            (controle2_content.strip(), patient_id)
        )
        BD.commit()
        controle2.destroy()
        alert("Success", "Data saved successfully")
    
    except Exception as e:
        alert("Error", f"Data not saved: {str(e)}")


# *************************************************************************************************************
# ********************************** Function to show consultation window *************************************
# *************************************************************************************************************

def show_control2():
    global controle2, combo_patient
    global entry_motif, entry_antecedent, entry_examen, entry_ordonnance, entry_bilan
    global entry_resultat, entry_specialiste, entry_avisspe, entry_controle1, entry_controle2

    controle2 = Tk()
    controle2.title("DOC HAJAR - Consultation Control")
    controle2.wm_iconbitmap('data/Hajar.ico')
    controle2.resizable(width=False, height=False)

    BD = sql.connect('data/DB.db')
    cur = BD.cursor()
    
    # Fetch patients' names and IDs
    cur.execute("SELECT ID, Nom, Prenom FROM Patients ORDER BY Nom")
    patients = cur.fetchall()
    patient_names = [f"{patient[0]} - {patient[1]} {patient[2]}" for patient in patients]

    # Define labels and fields
    label_patient = Label(controle2, text="Patient")
    label_motif = Label(controle2, text="Consultation Motive")
    label_antecedent = Label(controle2, text="Medical History")
    label_examen = Label(controle2, text="Examinations")
    label_ordonnance = Label(controle2, text="Prescription")
    label_bilan = Label(controle2, text="Requested Tests")
    label_resultat = Label(controle2, text="Test Results")
    label_specialiste = Label(controle2, text="Referred to Specialist")
    label_avisspe = Label(controle2, text="Specialist Opinion")
    label_controle1 = Label(controle2, text="First Control")
    label_controle2 = Label(controle2, text="Second Control")

    combo_patient = ttk.Combobox(controle2)
    combo_patient['values'] = patient_names

    entry_motif = Text(controle2, height=5, width=30)
    entry_antecedent = Text(controle2, height=5, width=30)
    entry_examen = Text(controle2, height=5, width=30)
    entry_ordonnance = Text(controle2, height=5, width=30)
    entry_bilan = Text(controle2, height=5, width=30)
    entry_resultat = Text(controle2, height=5, width=30)
    entry_specialiste = Entry(controle2)
    entry_avisspe = Text(controle2, height=5, width=30)
    entry_controle1 = Text(controle2, height=5, width=30)
    entry_controle2 = Text(controle2, height=5, width=30)

    button_save_to_db = Button(controle2, text="Save Data", command=save_record)
    button_get_data = Button(controle2, text="Fetch Info", command=get_info)

    # Grid layout for widgets
    label_patient.grid(column=1, row=1, padx=10, pady=10, columnspan=3, rowspan=2)
    label_motif.grid(column=1, row=4, padx=10, pady=10, columnspan=3, rowspan=6)
    label_antecedent.grid(column=1, row=10, padx=10, pady=10, columnspan=3, rowspan=6)
    label_examen.grid(column=16, row=4, padx=10, pady=10, columnspan=3, rowspan=6)
    label_ordonnance.grid(column=16, row=10, padx=10, pady=10, columnspan=3, rowspan=6)
    label_bilan.grid(column=1, row=28, padx=10, pady=10, columnspan=3, rowspan=6)
    label_resultat.grid(column=16, row=28, padx=10, pady=10, columnspan=3, rowspan=6)
    label_specialiste.grid(column=1, row=40, padx=10, pady=10, columnspan=3, rowspan=6)
    label_avisspe.grid(column=16, row=40, padx=10, pady=10, columnspan=3, rowspan=6)
    label_controle1.grid(column=1, row=52, padx=10, pady=10, columnspan=3, rowspan=6)
    label_controle2.grid(column=16, row=52, padx=10, pady=10, columnspan=3, rowspan=6)

    combo_patient.grid(column=5, row=1, padx=10, pady=10, columnspan=10, rowspan=2)
    button_get_data.grid(column=10, row=1, padx=10, pady=10, columnspan=10, rowspan=2)
    entry_motif.grid(column=5, row=4, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_antecedent.grid(column=5, row=10, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_examen.grid(column=22, row=4, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_ordonnance.grid(column=22, row=10, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_bilan.grid(column=5, row=28, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_resultat.grid(column=22, row=28, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_specialiste.grid(column=5, row=40, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_avisspe.grid(column=22, row=40, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_controle1.grid(column=5, row=52, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_controle2.grid(column=22, row=52, padx=10, pady=10, columnspan=10, rowspan=3)
    button_save_to_db.grid(column=15, row=60, padx=10, pady=10, columnspan=10, rowspan=3)

    controle2.mainloop()
