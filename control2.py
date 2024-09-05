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
    label_sexe = Label(control2, text=sexe)
    label_age = Label(control2, text=str(age) + " ans")
    label_sexe.grid(column=15, row=1, padx=10, pady=10, columnspan=10)
    label_age.grid(column=20, row=1, padx=10, pady=10, columnspan=10)
    stat3 = """ SELECT * FROM Consultations WHERE Patient_ID = """ + ID + """ ORDER BY Date_Consultation DESC"""
    cur.execute(stat3)
    try:
        data = cur.fetchall()[0]
        (date_consult, motif_consult, antecedent_consult, examens_consult,
         ordonance_consult, bilan_consult, resultats, specialiste_consult,
         avis_specialiste, control1_consult) = tuple(data[2:12])
        label_date_consultation = Label(
            control2,
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
        entry_control1.delete(0.0, END)

        entry_reason.insert(0.0, motif_consult)
        entry_history.insert(0.0, antecedent_consult)
        entry_exam.insert(0.0, examens_consult)
        entry_prescription.insert(0.0, ordonance_consult)
        entry_tests.insert(0.0, bilan_consult)
        entry_specialist.insert(0, specialiste_consult)
        entry_result.insert(0.0, resultats)
        entry_specialist_opinion.insert(0.0, avis_specialiste)
        entry_control1.insert(0.0, control1_consult)

    except Exception as e:
        alert("Error",
              f"Error: {str(e)},the patient didn't do any consultation")


def save_record():
    try:
        BD = sql.connect('data/data.db')
        cur = BD.cursor()
        consult_id = str(data[0])
        control2_content = get_text_from_text_widget(entry_control2, 0)
        stat = """ UPDATE Consultations SET Followup2 = """ + control2_content[:-2] + """ WHERE ID = """ + consult_id
        cur.execute(stat)
        BD.commit()
        control2.destroy()
        alert("Success", "Saved Successfully")
    except Exception as e:
        alert("Error",
              f"Error: {str(e)}, data not saved")


def show_control2():
    global control2, combo_patient
    global entry_reason, entry_history, entry_exam, entry_prescription
    global entry_tests, entry_result, entry_specialist, entry_specialist_opinion
    global entry_control1, entry_control2

    control2 = Tk()
    control2.title("DOC GESTURES - Control 2")
    control2.resizable(width=False, height=False)

    BD = sql.connect('data/data.db')
    cur = BD.cursor()
    stat3 = """SELECT ID, Last_Name, First_Name FROM Patients ORDER BY Last_Name"""
    cur.execute(stat3)
    patient_names = cur.fetchall()
    for i in range(len(patient_names)):
        patient_names[i] = str(patient_names[i][0]) + " - " + patient_names[i][1] + " " + patient_names[i][2]

    label_patient = Label(control2, text="Patient")
    label_reason = Label(control2, text="Consultation Reason")
    label_history = Label(control2, text="Medical History")
    label_exam = Label(control2, text="Exams")
    label_prescription = Label(control2, text="Prescription")
    label_tests = Label(control2, text="Requested Tests")
    label_result = Label(control2, text="Test Results")
    label_specialist = Label(control2, text="Referred to Specialist")
    label_specialist_opinion = Label(control2, text="Specialist Opinion")
    label_control1 = Label(control2, text="Control 1")
    label_control2 = Label(control2, text="Control 2")

    combo_patient = ttk.Combobox(control2)
    entry_reason = Text(control2, height=5, width=30)
    entry_history = Text(control2, height=5, width=30)
    entry_exam = Text(control2, height=5, width=30)
    entry_prescription = Text(control2, height=5, width=30)
    entry_tests = Text(control2, height=5, width=30)
    entry_result = Text(control2, height=5, width=30)
    entry_specialist = Entry(control2)
    entry_specialist_opinion = Text(control2, height=5, width=30)
    entry_control1 = Text(control2, height=5, width=30)
    entry_control2 = Text(control2, height=5, width=30)
    button_save_to_db = Button(control2, text="Save Data", command=save_record)
    button_get_data = Button(control2, text="Info", command=get_info)

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

    control2.mainloop()
