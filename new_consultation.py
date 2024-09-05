#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import datetime
from alert import alert
from get_data_from_widget import get_text_from_text_widget


def get_info():
    BD = sql.connect('data/data.db')
    cur = BD.cursor()

    try:
        patient_id = str(combo_patient.get()).split()[0]  # Extract patient ID
        cur.execute("SELECT Gender, Year_of_Birth FROM Patients WHERE ID = ?",
                    (patient_id,))
        result = cur.fetchone()

        if result:
            sexe, annee_naissance = result
            today = datetime.date.today()
            age = today.year - annee_naissance

            label_sexe = Label(Nouvelle_consult, text=sexe)
            label_age = Label(Nouvelle_consult, text=str(age) + " years old")

            label_sexe.grid(column=15, row=1, padx=10, pady=10, columnspan=10,
                            rowspan=2)
            label_age.grid(column=20, row=1, padx=10, pady=10, columnspan=10,
                           rowspan=2)
    except Exception as e:
        alert("Error", f"Failed to fetch patient data: {str(e)}")
    finally:
        BD.close()


def save_record():
    try:
        BD = sql.connect('data/data.db')
        cur = BD.cursor()

        patient_id = int(str(combo_patient.get()).split()[0])
        motif = get_text_from_text_widget(entry_motif, 0)
        antecedent = get_text_from_text_widget(entry_antecedent, 0)
        examen = get_text_from_text_widget(entry_examen, 0)
        ordonnance = get_text_from_text_widget(entry_ordonnance, 0)
        bilan = get_text_from_text_widget(entry_bilan, 0)
        specialiste = combo_specialiste.get()
        date_today = str(datetime.date.today())

        query = '''
            INSERT INTO Consultations
            (Patient_ID, Date_Consultation, Reason_for_Consultation,
            Medical_History, Examinations_and_Conclusions,
            Prescription, Requested_Tests, Referred_to_Specialist)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cur.execute(query, (patient_id, date_today, motif, antecedent,
                            examen, ordonnance, bilan, specialiste))
        BD.commit()

        Nouvelle_consult.destroy()
        alert("Success", "Data saved in the database")
    except Exception as e:
        alert("Error", f"Data not saved: {str(e)}")
    finally:
        BD.close()


def show_new_consult():
    global Nouvelle_consult, combo_patient
    global entry_motif, entry_antecedent, entry_examen, entry_ordonnance
    global entry_bilan, entry_resultat, combo_specialiste, entry_avisspe
    global entry_controle1, entry_controle2

    Nouvelle_consult = Tk()
    Nouvelle_consult.title("DOC GESTURES - Consultation")
    Nouvelle_consult.resizable(width=False, height=False)

    # Fetch patient data
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
        Label(Nouvelle_consult, text=text).grid(column=grid_pos[0],
                                                row=grid_pos[1],
                                                padx=10,
                                                pady=10,
                                                columnspan=3, rowspan=6)
    # Create Input Widgets
    combo_patient = ttk.Combobox(Nouvelle_consult, values=patients_list)
    combo_patient.grid(column=5, row=1, padx=10, pady=10, columnspan=10,
                       rowspan=2)

    entry_motif = Text(Nouvelle_consult, height=5, width=30)
    entry_antecedent = Text(Nouvelle_consult, height=5, width=30)
    entry_examen = Text(Nouvelle_consult, height=5, width=30)
    entry_ordonnance = Text(Nouvelle_consult, height=5, width=30)
    entry_bilan = Text(Nouvelle_consult, height=5, width=30)
    entry_resultat = Text(Nouvelle_consult, height=5, width=30)
    combo_specialiste = ttk.Combobox(Nouvelle_consult,
                                     values=['No',
                                             'Gastroenterologist',
                                             'Neurologist',
                                             'Cardiologist',
                                             'Dermatologist',
                                             'Ophthalmologist',
                                             'Endocrinologist',
                                             'Rheumatologist',
                                             'Gynecologist',
                                             'ENT Specialist',
                                             'Traumatologist',
                                             'Nephrologist',
                                             'Psychiatrist',
                                             'Pediatrician'])

    entry_avisspe = Text(Nouvelle_consult, height=5, width=30)
    entry_controle1 = Text(Nouvelle_consult, height=5, width=30)
    entry_controle2 = Text(Nouvelle_consult, height=5, width=30)

    # Place widgets
    entry_motif.grid(column=5, row=3, padx=10, pady=10, columnspan=10,
                     rowspan=3)
    entry_antecedent.grid(column=5, row=9, padx=10, pady=10, columnspan=10,
                          rowspan=3)
    entry_examen.grid(column=22, row=3, padx=10, pady=10, columnspan=10,
                      rowspan=3)
    entry_ordonnance.grid(column=22, row=9, padx=10, pady=10, columnspan=10,
                          rowspan=3)
    entry_bilan.grid(column=5, row=27, padx=10, pady=10, columnspan=10,
                     rowspan=3)
    entry_resultat.grid(column=22, row=27, padx=10, pady=10, columnspan=10,
                        rowspan=3)
    combo_specialiste.grid(column=5, row=39, padx=10, pady=10, columnspan=10,
                           rowspan=3)
    entry_avisspe.grid(column=22, row=39, padx=10, pady=10, columnspan=10,
                       rowspan=3)
    entry_controle1.grid(column=5, row=51, padx=10, pady=10, columnspan=10,
                         rowspan=3)
    entry_controle2.grid(column=22, row=51, padx=10, pady=10, columnspan=10,
                         rowspan=3)

    # Buttons
    button_save_to_db = Button(Nouvelle_consult, text="Save data",
                               command=save_record)
    button_save_to_db.grid(column=26, row=55, padx=10, pady=10, columnspan=10,
                           rowspan=2)

    button_get_data = Button(Nouvelle_consult, text="Info", command=get_info)
    button_get_data.grid(column=10, row=1, padx=10, pady=10, columnspan=10,
                         rowspan=2)

    Nouvelle_consult.mainloop()
