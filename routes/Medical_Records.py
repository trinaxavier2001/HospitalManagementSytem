from flask import Flask, render_template, request, redirect, flash
from models.medical_records import insertmedicalrecord, updatemedicalrecord, get_medical_records, deletemedicalrecord
from datetime import datetime

def med_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch medical records from the database
        medical_records = get_medical_records()
 
        # Render the template with the list of medical records
        return render_template('/MedicalRecords/Med.html', medical_records=medical_records)
    
    elif request.method == 'POST':
        action = request.form.get('action')
        if(action == 'insertrecord'):
            return render_template('/MedicalRecords/insert_medical_record.html')
            
        elif(action == 'insert'):
            # Process form submission and insert data into the medical_records table
            patient_id = int(request.form.get("patient_id"))
            doctor_id = int(request.form.get("doctor_id"))
            visit_date = request.form.get("visit_date")
            diagnosis = request.form.get("diagnosis")
        
            # Call the insert_medical_record method
            res = insertmedicalrecord(db, patient_id, doctor_id, visit_date, diagnosis)


        elif action == 'update':
            record_id = int(request.form.get('record_id'))
            # Get the updated information for the medical record from the form data
            updated_patient_id = int(request.form.get('patient_id'))
            updated_doctor_id = int(request.form.get('doctor_id'))
            updated_visit_date = request.form.get('visitdate')
            updated_diagnosis = request.form.get('details')
 
            # Update the medical record in the database
            res = updatemedicalrecord(db, updated_patient_id, updated_doctor_id, updated_visit_date, updated_diagnosis)
            
            if res:
                flash('Update successful!', 'success')
            else:
                flash('Update Unsuccessful!', 'error')
 
        elif action == 'delete':
            record_id = int(request.form.get('record_id'))
            # Delete the medical record from the database
            res = deletemedicalrecord(db, record_id)
            
            if res:
                flash('Delete successful!', 'success')
            else:
                flash('Delete Unsuccessful!', 'error')
 
    # Redirect to the same page to refresh the medical record list
    return redirect('/med')
