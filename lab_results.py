#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import datetime

from alert import *
from get_data_from_widget import *

def get_info():
    global data
    BD = sql.connect('data/data.db')
    cur = BD.cursor()
    patient = str(combo_patient.get())
    stat1 = """ SELECT Gender FROM Patients WHERE ID = """ + patient.split()[0]
    stat2 = """ SELECT Year_of_Birth FROM Patients WHERE ID = """ + patient.split()[0]
    cur.execute(stat1)
    sexe = cur.fetchall()[0][0]
    cur.execute(stat2)
    annee = cur.fetchall()[0][0]
    today = datetime.date.today()
    year = today.year
    age = year - annee
    label_sexe = Label(resultat_bilan, text = sexe)
    label_age = Label(resultat_bilan, text = str(age) + " ans")
    label_sexe.grid(column=15, row=1, padx=10, pady=10,columnspan=10)
    label_age.grid(column=20, row=1, padx=10, pady=10,columnspan=10)
    stat3 = """ SELECT * FROM Consultations WHERE ID = """ + patient.split()[0] + """ ORDER BY Date_Consultation DESC"""
    cur.execute(stat3)
    try:
        data = cur.fetchall()[0]
        date_consult, motif_consult, antecedent_consult, examens_consult, ordonance_consult, bilan_consult  = tuple(data[2:8])
        specialiste_consult = data[9]
        label_date_consultation = Label(resultat_bilan, text = "Date of the last consultation : " + date_consult)
        label_date_consultation.grid(column=20, row=2, padx=10, pady=10,columnspan=10)

        entry_motif.delete(0.0,END)
        entry_antecedent.delete(0.0,END)
        entry_examen.delete(0.0,END)
        entry_ordonnance.delete(0.0,END)
        entry_bilan.delete(0.0,END)
        entry_specialiste.delete(0,END)
        
        entry_motif.insert(0.0,motif_consult)
        entry_antecedent.insert(0.0,antecedent_consult)
        entry_examen.insert(0.0,examens_consult)
        entry_ordonnance.insert(0.0,ordonance_consult)
        entry_bilan.insert(0.0,bilan_consult)
        entry_specialiste.insert(0,specialiste_consult)
    except Exception as e:
        alert("Error",f"Error: {str(e)}, the patient didn't do any consultation")
    
    
def save_record():
    try:
        BD = sql.connect('data/data.db')
        cur = BD.cursor()
        ID = str(data[0])
        bilan_res = get_text_from_text_widget(entry_resultat,0)
        specialiste_avis = get_text_from_text_widget(entry_avisspe,0)
        stat = """ UPDATE Consultations SET Test_Results = """ + bilan_res + """ Specialist_Advice = """ + specialiste_avis[:-2] + """ WHERE ID = """ + ID
        cur.execute(stat)
        BD.commit()
        resultat_bilan.destroy()
        alert("Success","Data saved in the database")
    except Exception as e:
        alert("Error",f"Error: {str(e)}, data not saved")


def show_resultat_bilan():

    global resultat_bilan, combo_patient
    global entry_motif, entry_antecedent, entry_examen, entry_ordonnance, entry_bilan
    global entry_resultat, entry_specialiste, entry_avisspe, entry_controle1, entry_controle2

    resultat_bilan = Tk()
    resultat_bilan.title("DOC GESTURES - Test Results / Specialist advice")
    resultat_bilan.resizable(width=False, height=False)

    BD = sql.connect('data/data.db')
    cur = BD.cursor()
    query = "SELECT ID, Last_Name, First_Name FROM Patients ORDER BY Last_Name"
    cur.execute(query)
    Noms = cur.fetchall()
    BD.close()

    patients_list = [f"{row[0]} - {row[1]} {row[2]}" for row in Noms]

    # Create Labels
    labels = {"Patient": (1, 1),
              "Reason for Consultation": (1, 3),
              "Medical History": (1, 9),
              "Examinations": (16, 3),
              "Prescription": (16, 9),
              "Requested Tests": (1, 27),
              "Test Results": (16, 27),
              "Referred to Specialist": (1, 39),
              "Specialist's Opinion": (16, 39),
              "Follow-up 1": (1, 51),
              "Follow-up 2": (16, 51)}

    for text, grid_pos in labels.items():
        Label(resultat_bilan, text=text).grid(column=grid_pos[0],
                                                row=grid_pos[1],
                                                padx=10,
                                                pady=10,
                                                columnspan=3, rowspan=6)

    combo_patient = ttk.Combobox(resultat_bilan)
    entry_motif = Text(resultat_bilan, height = 5, width = 30)
    entry_antecedent = Text(resultat_bilan, height = 5, width = 30)
    entry_examen = Text(resultat_bilan, height = 5, width = 30)
    entry_ordonnance = Text(resultat_bilan, height = 5, width = 30)
    entry_bilan = Text(resultat_bilan, height = 5, width = 30)
    entry_resultat = Text(resultat_bilan, height = 5, width = 30)
    entry_specialiste = Entry(resultat_bilan)
    entry_avisspe = Text(resultat_bilan, height = 5, width = 30)
    entry_controle1 = Text(resultat_bilan, height = 5, width = 30)
    entry_controle2 = Text(resultat_bilan, height = 5, width = 30)
    button_save_to_db = Button(resultat_bilan, text = "Save data",command = save_record )
    button_get_data = Button(resultat_bilan, text = "Info",command = get_info )
    
    combo_patient['values'] = patients_list
    button_get_data.grid(column=10, row=1, padx=10, pady=10,columnspan=10, rowspan = 2)
    entry_motif.grid(column=5, row=4, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_antecedent.grid(column=5, row=10, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_examen.grid(column=22, row=4, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_ordonnance.grid(column=22, row=10, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_bilan.grid(column=5, row=28, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_resultat.grid(column=22, row=28, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_specialiste.grid(column=5, row=40, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_avisspe.grid(column=22, row=40, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_controle1.grid(column=5, row=52, padx=10, pady=10,columnspan=10, rowspan = 3)
    entry_controle2.grid(column=22, row=52, padx=10, pady=10,columnspan=10, rowspan = 3)
    button_save_to_db.grid(column=26, row=56, padx=10, pady=10,columnspan=10, rowspan = 2)
    combo_patient.grid(column=5, row=1, padx=10, pady=10,columnspan=10, rowspan = 2)

    resultat_bilan.mainloop()

show_resultat_bilan()