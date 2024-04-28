from flask import Flask, render_template, request, redirect, flash, url_for
from models.patient import insertpatient, updatepatient, get_patient_records, deletepatient
from datetime import datetime


def pat_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch patient records from the database
        patients = get_patient_records()
 
        # Render the template with the list of patients
        return render_template('/Patient/Pat.html', patients=patients)
    
    elif request.method == 'POST':
        action = request.form.get('action')
        if(action == 'insertrecord'):
            return render_template('/Patient/insert_patient.html')

        elif(action == 'insert'):
            # Process form submission and insert data into the patient table
            patient_id = int(request.form.get("patient_id"))
            doctor_id = int(request.form.get("doctor_id"))
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            dob = request.form.get("dob")
            gender = request.form.get("gender")
            address = request.form.get("address")
            phone = request.form.get("phone")
            email = request.form.get("email")
            emergency_contact_name = request.form.get("emergency_contact_name")
            emergency_contact_phone = request.form.get("emergency_contact_phone")
            insurance_company = request.form.get("insurance_company")
            insurance_policy_number = request.form.get("insurance_policy_number")
            medical_history_summary = request.form.get("medical_history_summary")
            current_medications = request.form.get("current_medications")
            
            # Call the insert_patient method
            res = insertpatient(db,patient_id,doctor_id, first_name, last_name, dob, gender, address, phone, email, emergency_contact_name, emergency_contact_phone, insurance_company, insurance_policy_number, medical_history_summary, current_medications)
            return redirect(url_for('success', message=res))
            # return redirect('/dep')
        
        if action == 'update':
            patient_id = int(request.form.get('patient_id'))
            # Get the updated information for the patient from the form data
            updated_first_name = request.form.get('FirstName')
            updated_last_name = request.form.get('LastName')
            updated_doctor_id = int(request.form.get('doctor_id'))
            updated_dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d')
            updated_gender = request.form.get('Gender')
            updated_address = request.form.get('Address')
            updated_phone = request.form.get('Phone')
            updated_email = request.form.get('Email')
            updated_emergency_contact_name = request.form.get('EmergencyContactName')
            updated_emergency_contact_phone = request.form.get('EmergencyContactPhone')
            updated_insurance_company = request.form.get('InsuranceCompany')
            updated_insurance_policy_number = request.form.get('InsurancePolicyNumber')
            updated_medical_history_summary = request.form.get('MedicalHistorySummary')
            updated_current_medication = request.form.get('CurrentMedication')
 
            # Update the patient's record in the database
            res = updatepatient(db, patient_id, updated_first_name, updated_last_name, updated_doctor_id,
                                  updated_dob, updated_gender, updated_address, updated_phone, updated_email,
                                  updated_emergency_contact_name, updated_emergency_contact_phone,
                                  updated_insurance_company, updated_insurance_policy_number,
                                  updated_medical_history_summary, updated_current_medication)
            
            if res:
                flash('Update successful!', 'success')
            else:
                flash('Update Unsuccessful!', 'error')
 
        elif action == 'delete':
            patient_id = int(request.form.get('patient_id'))
            # Delete the patient's record from the database
            res = deletepatient(db, patient_id)
            
            if res:
                flash('Delete successful!', 'success')
            else:
                flash('Delete Unsuccessful!', 'error')
 
    # Redirect to the same page to refresh the patient list
    return redirect('/pat')
