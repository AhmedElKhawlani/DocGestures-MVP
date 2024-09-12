# DocGestures-MVP
# DOC GESTURES - Clinic Management

## Overview
DOC GESTURES is a clinic management application designed to help doctors manage patients, consultations, lab results, and follow-up controls efficiently. The application provides an easy-to-use graphical interface built using Python's Tkinter library and integrates a SQLite database to store and retrieve patient and consultation data.

## Features

1. **Add New Patient**: 
   - Allows doctors to input and store new patient information in the database.

2. **New Consultation**: 
   - Provides a form for starting a new consultation where the doctor can record the patient's symptoms, medical history, prescriptions, and more.

3. **Lab Results and Specialist Opinion**: 
   - Doctors can view and update the patient's test results and record any specialist's advice related to the patient's condition.

4. **First and Second Follow-up Controls**: 
   - Manage follow-up consultations, enabling doctors to track a patient’s progress over time.

## Main Modules

### 1. **Main Application Window**:
   - The primary interface presents buttons for each main action: Adding patients, starting a new consultation, viewing lab results, and managing follow-ups.

### 2. **Add Patient**:
   - Opens a window to add a new patient with their relevant details stored in the `Patients` table of the database.

### 3. **New Consultation**:
   - A form for doctors to enter detailed consultation information (motif, antecedents, examinations, prescriptions, etc.). This data is saved into the `Consultations` table of the database.

### 4. **Lab Results and Specialist Opinions**:
   - Displays past consultation details and allows the doctor to add or update lab test results and any specialist advice for the patient.

### 5. **Follow-up Controls**:
   - Two distinct forms for tracking follow-up appointments and progress after the first and second consultations.

## Database Structure

The application uses a SQLite database (`data/data.db`) to store the following tables:

- **Patients**: Stores patient data such as ID, name, gender, and year of birth.
- **Consultations**: Records details of each consultation, including the reason for consultation, medical history, prescriptions, and lab results.

## How to Run

1. Install the required dependencies:
   - Tkinter (bundled with most Python distributions)
   - SQLite3 (also included in Python)

2. Run the main application:
   ```bash
   python3 main_window.py

