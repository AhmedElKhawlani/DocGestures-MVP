#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import datetime

from Alerte import *
from Get_Data_From_Widget import *

#*************************************************************************************************************
#****************************************** function get_info ************************************************
#*************************************************************************************************************    

def get_info():
    global data
    BD = sql.connect('data/DOC HAJAR.db')
    cur = BD.cursor()
    patient = str(combo_patient.get())
    stat1 = """ SELECT SEXE FROM Patients WHERE ID = """ + patient.split()[0]
    stat2 = """ SELECT ANNEE_NAISSANCE FROM Patients WHERE ID = """ + patient.split()[0]
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
    stat3 = """ SELECT * FROM Consultations WHERE ID_Patient = """ + patient.split()[0] + """ ORDER BY Date_Consultation DESC"""
    cur.execute(stat3)
    try:
        data = cur.fetchall()[0]
        date_consult, motif_consult, antecedent_consult, examens_consult, ordonance_consult, bilan_consult  = tuple(data[2:8])
        specialiste_consult = data[9]
        label_date_consultation = Label(resultat_bilan, text = "Date de la dernière consultation : " + date_consult)
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
    except:
        alerte("Erreur","Le patient n'a effectué aucune consultation")
    
    
#*************************************************************************************************************
#*********************************** save consult data into database *****************************************
#************************************************************************************************************* 

def save_record():
    #try:
    BD = sql.connect('data/DOC HAJAR.db')
    cur = BD.cursor()
    ID = str(data[0])
    bilan_res = get_text_from_Text(entry_resultat,0)
    specialiste_avis = get_text_from_Text(entry_avisspe,0)
    stat = """ UPDATE Consultations SET Résultats_bilans = """ + bilan_res + """ Avis_spécialiste = """ + specialiste_avis[:-2] + """ WHERE ID = """ + ID
    cur.execute(stat)
    BD.commit()
    resultat_bilan.destroy()
    alerte("Succés","Enregistrées Avec Succés")
    #except:
        #alerte("Erreur","Données non enregistrées")

#*************************************************************************************************************
#****************************** Function to show resultat_bilan window ***************************************
#*************************************************************************************************************

def show_resultat_bilan():

    global resultat_bilan, combo_patient
    global entry_motif, entry_antecedent, entry_examen, entry_ordonnance, entry_bilan
    global entry_resultat, entry_specialiste, entry_avisspe, entry_controle1, entry_controle2

    resultat_bilan = Tk()
    resultat_bilan.title("DOC HAJAR - Résultats Bilans / Avis spécialiste")
    resultat_bilan.wm_iconbitmap('data/Hajar.ico')
    resultat_bilan.resizable(width=False, height=False)

    BD = sql.connect('data/DOC HAJAR.db')
    cur = BD.cursor()
    stat3 = """SELECT ID, Nom, Prenom From Patients ORDER BY Nom"""
    cur.execute(stat3)
    Noms = cur.fetchall()
    for i in range(len(Noms)):
        Noms[i] = str(Noms[i][0]) + " - " + Noms[i][1] + " " + Noms[i][2]

    label_patient = Label(resultat_bilan,text = "Patient")
    label_motif = Label(resultat_bilan,text = "Motif de Consultation")
    label_antecedent = Label(resultat_bilan,text = "Antécédents")
    label_examen = Label(resultat_bilan,text = "Examens")
    label_ordonnance = Label(resultat_bilan,text = "Ordonnance")
    label_bilan = Label(resultat_bilan,text = "Bilans demandés")
    label_resultat = Label(resultat_bilan,text = "Résultats des bilans")
    label_specialiste = Label(resultat_bilan,text = "Envoyé vers un spécialiste")
    label_avisspe = Label(resultat_bilan,text = "Avis spécialiste")
    label_controle1 = Label(resultat_bilan,text = "Controle 1")
    label_controle2 = Label(resultat_bilan,text = "Controle 2")

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
    button_save_to_db = Button(resultat_bilan, text = "Enregistrer les données",command = save_record )
    button_get_data = Button(resultat_bilan, text = "Info",command = get_info )

    label_patient.grid(column=1, row=1, padx=10, pady=10,columnspan=3, rowspan = 2)
    label_motif.grid(column=1, row=4, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_antecedent.grid(column=1, row=10, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_examen.grid(column=16, row=4, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_ordonnance.grid(column=16, row=10, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_bilan.grid(column=1, row=28, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_resultat.grid(column=16, row=28, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_specialiste.grid(column=1, row=40, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_avisspe.grid(column=16, row=40, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_controle1.grid(column=1, row=52, padx=10, pady=10,columnspan=3, rowspan = 6)
    label_controle2.grid(column=16, row=52, padx=10, pady=10,columnspan=3, rowspan = 6)
    
    combo_patient['values'] = Noms
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
