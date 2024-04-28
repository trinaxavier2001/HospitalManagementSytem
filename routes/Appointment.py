from flask import get_flashed_messages, render_template, request, redirect, flash, url_for
from pymongo import MongoClient
from datetime import datetime
from models.appointment import insertappointment, updateappointment, get_appointment_records, deleteappointment

def appo_record1(db,messages):
        # Assuming you have a function to fetch appointment records from the database
        appointments = get_appointment_records()

        # Render the template with the list of appointments
        return render_template('/Appointment/Appo1.html', appointments=appointments, messages=messages)


def appo_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch appointment records from the database
        appointments = get_appointment_records()
        # Render the template with the list of appointments
        return render_template('/Appointment/Appoedit.html', appointments=appointments)
    
    elif request.method == 'POST':
        action = request.form.get('action')
        if action == 'insertrecord':
            return render_template('/Appointment/insert-record.html')
        
        elif action == 'insert':
            patient_id = int(request.form.get('patient_id'))
            # Get the updated information for the appointment from the form data
            updated_datetime = request.form.get('datetime')
            updated_purpose = request.form.get('purpose')
            updated_doctor_id = int(request.form.get('doctor_id'))

            # Call the insertRecord method with the updated data
            res = insertappointment(patient_id,updated_doctor_id, updated_datetime, updated_purpose, 'Scheduled')
            result = res.split()[-1]
            if result:
                flash('Insert successful!', 'success')
                
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Insert Unsuccessful!\n' + res, 'error')
            return redirect(url_for('appo1', messages='_'.join(get_flashed_messages())))
            
        
        elif action == 'update':
            appointment_id = int(request.form.get('appointment_id'))
            patient_id = int(request.form.get('patient_id'))
            # Get the updated information for the appointment from the form data
            # Get the datetime string from the form
            raw_datetime = request.form.get('datetime')

            # Remove the ":00" from the end of the string if present (assuming seconds are always ":00")
            cleaned_datetime = raw_datetime[:-3]

            # Parse the cleaned datetime string into a datetime object
            updated_datetime = datetime.strptime(cleaned_datetime, '%Y-%m-%d %H:%M')
            # updated_datetime = datetime.strptime(request.form.get('datetime'), '%Y-%m-%d %H:%M')
            updated_purpose = request.form.get('purpose')
            updated_status = request.form.get('status')
            updated_doctor_id = int(request.form.get('doctor_id'))

            # Update the appointment's record in the database
            res = updateappointment(db, appointment_id, patient_id, updated_doctor_id ,updated_datetime, updated_purpose, updated_status)
            result = res.split()[-1]
            print('coming')
            if result:
                flash('Update successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Update Unsuccessful!\n' + res, 'error')
                print('entered')
            return redirect(url_for('appo1', messages='_'.join(get_flashed_messages())))
            

        elif action == 'delete':
            appointment_id = int(request.form.get('appointment_id'))
            patient_id = int(request.form.get('patient_id'))
            # Delete the appointment's record from the database
            res = deleteappointment(db, appointment_id, patient_id)
            result = res.split()[-1]

            if result:
                flash('Delete successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Delete Unsuccessful!\n' + res, 'error')
            return redirect(url_for('appo1', messages='_'.join(get_flashed_messages())))

    # Redirect to the same page to refresh the appointment list
    # return redirect('/appo1',method='GET')
