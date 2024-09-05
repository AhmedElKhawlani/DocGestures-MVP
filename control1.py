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
    ID = patient.split()[0]
    stat1 = " SELECT Gender FROM Patients WHERE ID = " + ID
    stat2 = " SELECT Year_of_Birth FROM Patients WHERE ID = " + ID
    cur.execute(stat1)
    sexe = cur.fetchall()[0][0]
    cur.execute(stat2)
    annee = cur.fetchall()[0][0]
    today = datetime.date.today()
    year = today.year
    age = year - annee
    label_sexe = Label(control1, text=sexe)
    label_age = Label(control1, text=str(age) + " ans")
    label_sexe.grid(column=15, row=1, padx=10, pady=10, columnspan=10)
    label_age.grid(column=20, row=1, padx=10, pady=10, columnspan=10)
    stat3 = """ SELECT * FROM Consultations WHERE Patient_ID = """ + ID + """ ORDER BY Date_Consultation DESC"""
    cur.execute(stat3)
    try:
        data = cur.fetchall()[0]
        (date_consult, motif_consult, antecedent_consult, examens_consult,
         ordonance_consult, bilan_consult, resultats, specialiste_consult,
         avis_specialiste) = tuple(data[2:11])
        label_date_consultation = Label(
            control1,
            text="Date of the last consultation : " + date_consult
        )
        label_date_consultation.grid(column=20, row=2, padx=10, pady=10,
                                     columnspan=10)

        entry_reason.delete(0.0, END)
        entry_history.delete(0.0, END)
        entry_exam.delete(0.0, END)
        entry_prescription.delete(0.0, END)
        entry_tests.delete(0.0, END)
        entry_specialist.delete(0, END)
        entry_result.delete(0.0, END)
        entry_specialist_opinion.delete(0.0, END)

        entry_reason.insert(0.0, motif_consult)
        entry_history.insert(0.0, antecedent_consult)
        entry_exam.insert(0.0, examens_consult)
        entry_prescription.insert(0.0, ordonance_consult)
        entry_tests.insert(0.0, bilan_consult)
        entry_specialist.insert(0, specialiste_consult)
        entry_result.insert(0.0, resultats)
        entry_specialist_opinion.insert(0.0, avis_specialiste)

    except Exception as e:
        alert("Error",
              f"Error: {str(e)},the patient didn't do any consultation")


def save_record():
    try:
        BD = sql.connect('data/data.db')
        cur = BD.cursor()
        consult_id = str(data[0])
        control1_content = get_text_from_text_widget(entry_control1, 0)
        stat = """ UPDATE Consultations SET Followup1 = """ + control1_content[:-2] + """ WHERE ID = """ + consult_id
        cur.execute(stat)
        BD.commit()
        control1.destroy()
        alert("Success", "Saved Successfully")
    except Exception as e:
        alert("Error",
              f"Error: {str(e)}, data not saved")


def show_control1():
    global control1, combo_patient
    global entry_reason, entry_history, entry_exam, entry_prescription, entry_tests
    global entry_result, entry_specialist, entry_specialist_opinion, entry_control1, entry_control2

    control1 = Tk()
    control1.title("DOC GESTURES - Control 1")
    control1.resizable(width=False, height=False)

    BD = sql.connect('data/data.db')
    cur = BD.cursor()
    stat3 = """SELECT ID, Last_Name, First_Name FROM Patients ORDER BY Last_Name"""
    cur.execute(stat3)
    patient_names = cur.fetchall()
    for i in range(len(patient_names)):
        patient_names[i] = str(patient_names[i][0]) + " - " + patient_names[i][1] + " " + patient_names[i][2]

    label_patient = Label(control1, text="Patient")
    label_reason = Label(control1, text="Consultation Reason")
    label_history = Label(control1, text="Medical History")
    label_exam = Label(control1, text="Exams")
    label_prescription = Label(control1, text="Prescription")
    label_tests = Label(control1, text="Requested Tests")
    label_result = Label(control1, text="Test Results")
    label_specialist = Label(control1, text="Referred to Specialist")
    label_specialist_opinion = Label(control1, text="Specialist Opinion")
    label_control1 = Label(control1, text="Control 1")
    label_control2 = Label(control1, text="Control 2")

    combo_patient = ttk.Combobox(control1)
    entry_reason = Text(control1, height=5, width=30)
    entry_history = Text(control1, height=5, width=30)
    entry_exam = Text(control1, height=5, width=30)
    entry_prescription = Text(control1, height=5, width=30)
    entry_tests = Text(control1, height=5, width=30)
    entry_result = Text(control1, height=5, width=30)
    entry_specialist = Entry(control1)
    entry_specialist_opinion = Text(control1, height=5, width=30)
    entry_control1 = Text(control1, height=5, width=30)
    entry_control2 = Text(control1, height=5, width=30)
    button_save_to_db = Button(control1, text="Save Data", command=save_record)
    button_get_data = Button(control1, text="Info", command=get_info)

    # Grid layout
    label_patient.grid(column=1, row=1, padx=10, pady=10, columnspan=3,
                       rowspan=2)
    label_reason.grid(column=1, row=4, padx=10, pady=10, columnspan=3, rowspan=6)
    label_history.grid(column=1, row=10, padx=10, pady=10, columnspan=3, rowspan=6)
    label_exam.grid(column=16, row=4, padx=10, pady=10, columnspan=3, rowspan=6)
    label_prescription.grid(column=16, row=10, padx=10, pady=10, columnspan=3, rowspan=6)
    label_tests.grid(column=1, row=28, padx=10, pady=10, columnspan=3, rowspan=6)
    label_result.grid(column=16, row=28, padx=10, pady=10, columnspan=3, rowspan=6)
    label_specialist.grid(column=1, row=40, padx=10, pady=10, columnspan=3, rowspan=6)
    label_specialist_opinion.grid(column=16, row=40, padx=10, pady=10, columnspan=3, rowspan=6)
    label_control1.grid(column=1, row=52, padx=10, pady=10, columnspan=3, rowspan=6)
    label_control2.grid(column=16, row=52, padx=10, pady=10, columnspan=3, rowspan=6)

    combo_patient['values'] = patient_names
    button_get_data.grid(column=10, row=1, padx=10, pady=10, columnspan=10, rowspan=2)
    entry_reason.grid(column=5, row=4, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_history.grid(column=5, row=10, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_exam.grid(column=22, row=4, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_prescription.grid(column=22, row=10, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_tests.grid(column=5, row=28, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_result.grid(column=22, row=28, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_specialist.grid(column=5, row=40, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_specialist_opinion.grid(column=22, row=40, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_control1.grid(column=5, row=52, padx=10, pady=10, columnspan=10, rowspan=3)
    entry_control2.grid(column=22, row=52, padx=10, pady=10, columnspan=10, rowspan=3)
    button_save_to_db.grid(column=26, row=56, padx=10, pady=10, columnspan=10, rowspan=2)
    combo_patient.grid(column=5, row=1, padx=10, pady=10, columnspan=10, rowspan=2)

    control1.mainloop()
