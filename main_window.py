#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import sqlite3 as sql
import datetime

# Importing functions from other modules
from add_patient import show_add_patient_window
from new_consultation import show_nouvelle_consult
from lab_results import show_resultat_bilan
from control1 import show_control1
from control2 import show_control2

# Create main window
principale = Tk()
principale.title("DOC HAJAR - Clinic Management")
principale.resizable(width=False, height=False)

# Define buttons
button_add_patient = Button(principale, text="Add New Patient", command=show_add_patient_window)
button_new_consultation = Button(principale, text="New Consultation", command=show_nouvelle_consult)
button_results = Button(principale, text="Test Results / Specialist Opinion", command=show_resultat_bilan)
button_control1 = Button(principale, text="First Control", command=show_control1)
button_control2 = Button(principale, text="Second Control", command=show_control2)

# Adjust spacing with empty labels
label_adjust_top = Label(principale, text=" ")
label_adjust_side = Label(principale, text=" ")

# Grid layout for spacing
label_adjust_top.grid(column=1, row=1, padx=10, pady=10, columnspan=3)
label_adjust_side.grid(column=8, row=1, padx=10, pady=10, columnspan=3)

# Grid layout for buttons
button_add_patient.grid(column=4, row=1, padx=10, pady=10, columnspan=4)
button_new_consultation.grid(column=4, row=2, padx=10, pady=10, columnspan=4)
button_results.grid(column=4, row=3, padx=10, pady=10, columnspan=4)
button_control1.grid(column=4, row=4, padx=10, pady=10, columnspan=4)
button_control2.grid(column=4, row=5, padx=10, pady=10, columnspan=4)

# Start the GUI loop
principale.mainloop()
