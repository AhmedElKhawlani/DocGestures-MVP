#!/usr/bin/python3

import sqlite3

path = 'data/data.db'

db = sqlite3.connect(path)

cursor = db.cursor()

# Create the 'Patients' table
cursor.execute('''
    CREATE TABLE Patients (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Last_Name TEXT,
        First_Name TEXT,
        Gender TEXT,
        Year_of_Birth INTEGER
    );
''')

# Create the 'Consultations' table
cursor.execute('''
    CREATE TABLE Consultations (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Patient_ID INTEGER,
        Date_Consultation DATE,
        Reason_for_Consultation TEXT,
        Medical_History TEXT,
        Examinations_and_Conclusions TEXT,
        Prescription TEXT,
        Requested_Tests TEXT,
        Test_Results TEXT,
        Referred_to_Specialist TEXT,
        Specialist_Advice TEXT,
        Followup1 TEXT,
        Followup2 TEXT,
        FOREIGN KEY(Patient_ID) REFERENCES Patients(ID)
    );
''')

db.commit()
db.close()
