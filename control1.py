#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import datetime

from alert import *
from get_data_from_widget import *

# ************************************************************************************************************
# ****************************************** Function to get info *********************************************
# ************************************************************************************************************


def get_info():
    global data
    BD = sql.connect('data/DOC HAJAR.db')
    cur = BD.cursor()
    patient = str(combo_patient.get())
    stat1 = """ SELECT SEX FROM Patients WHERE ID = """ + patient.split()[0]
    stat2 = """ SELECT BIRTH_YEAR FROM Patients WHERE ID = """ + patient.split()[0]
    cur.execute(stat1)
    sex = cur.fetchall()[0][0]
    cur.execute(stat2)
    birth_year = cur.fetchall()[0][0]
    today = datetime.date.today()
    current_year = today.year
    age = current_year - birth_year
    label_sex = Label(control1, text=sex)
    label_age = Label(control1, text=str(age) + " years")
    label_sex.grid(column=15, row=1, padx=10, pady=10, columnspan=10)
    label_age.grid(column=20, row=1, padx=10, pady=10, columnspan=10)

    stat3 = """ SELECT * FROM Consultations WHERE Patient_ID = """ + patient.split()[0] + """ ORDER BY Consultation_Date DESC"""
    cur.execute(stat3)

    try:
        data = cur.fetchall()[0]
        (consultation_date, consultation_reason, history, exams, prescription,
         requested_tests, results, specialist, specialist_opinion) = tuple(data[2:11])

        label_last_consultation = Label(
            control1, text="Last Consultation Date: " + consultation_date)
        label_last_consultation.grid(column=20, row=2, padx=10, pady=10, columnspan=10)

        entry_reason.delete(0.0, END)
        entry_history.delete(0.0, END)
        entry_exam.delete(0.0, END)
        entry_prescription.delete(0.0, END)
        entry_tests.delete(0.0, END)
        entry_specialist.delete(0, END)
        entry_result.delete(0.0, END)
        entry_specialist_opinion.delete(0.0, END)

        entry_reason.insert(0.0, consultation_reason)
        entry_history.insert(0.0, history)
        entry_exam.insert(0.0, exams)
        entry_prescription.insert(0.0, prescription)
        entry_tests.insert(0.0, requested_tests)
        entry_specialist.insert(0, specialist)
        entry_result.insert(0.0, results)
        entry_specialist_opinion.insert(0.0, specialist_opinion)
    except:
        alert("Error", "The patient has not had any consultation yet")

# ************************************************************************************************************
# ********************************* Save consult data into the database **************************************
# ************************************************************************************************************


def save_record():
    try:
        BD = sql.connect('data/DOC HAJAR.db')
        cur = BD.cursor()
        patient_id = str(data[0])
        control1_content = get_text_from_text_widget(entry_control1, 0)
        stat = """ UPDATE Consultations SET Control1 = """ + control1_content[:-2] + """ WHERE ID = """ + patient_id
        cur.execute(stat)
        BD.commit()
        control1.destroy()
        alert("Success", "Saved Successfully")
    except:
        alert("Error", "Data not saved")


# ************************************************************************************************************
# ************************************ Function to show control1 window ***************************************
# ************************************************************************************************************


def show_control1():
    global control1, combo_patient
    global entry_reason, entry_history, entry_exam, entry_prescription, entry_tests
    global entry_result, entry_specialist, entry_specialist_opinion, entry_control1, entry_control2

    control1 = Tk()
    control1.title("DOC HAJAR - Control 1")
    control1.wm_iconbitmap('data/Hajar.ico')
    control1.resizable(width=False, height=False)

    BD = sql.connect('data/DB.db')
    cur = BD.cursor()
    stat3 = """SELECT ID, LastName, FirstName FROM Patients ORDER BY LastName"""
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
    label_patient.grid(column=1, row=1, padx=10, pady=10, columnspan=3, rowspan=2)
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
