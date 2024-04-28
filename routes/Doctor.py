from flask import Flask, render_template, request, redirect, jsonify, url_for, json, flash
import csv
from pymongo import MongoClient
from datetime import datetime
from models.doctor import insertdoctor, updatedoctor, deletedoctor, get_doctors_records


def doc_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch doctors' records from the database
        doctors = get_doctors_records()

        # Render the template with the list of doctors
        return render_template('/Doctor/Doc.html', doctors=doctors)
 
    elif request.method == 'POST':
        action = request.form.get('action')
        print(action)
        if(action == 'insertrecord'):
            return render_template('/Doctor/insert_doctor.html')
        
        elif(action == 'insert'):
            # Process form submission and insert data into the doctor table
            employee_id = int(request.form.get("employee_id"))
            specialization = request.form.get("specialization")
            # Call the insert_doctor method
            print(employee_id)
            res = insertdoctor(db, employee_id, specialization)
            if res:
                flash('Update successful!'+res, 'success')
            else:
                flash('Error'+res,'error')
            return redirect('/doc')

        elif action == 'update':
            doctor_id = int(request.form.get('doctor_id'))
            # Get the updated information for the doctor from the form data
            updated_employeeid = int(request.form.get('employee_id'))
            updated_specialization = request.form.get('specialization')
            print(doctor_id,updated_employeeid, updated_specialization)
            # Update the doctor's record in the database
            res = updatedoctor(db,doctor_id,updated_employeeid, updated_specialization)
            result = res.split()[-1]
            # return res
            if(result):
                flash('Update successful!', 'success')
                return redirect('/doc')
                
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts) 
                flash('Update Unsuccessful!/n'+res, 'error')
                return redirect('/doc')
                
            # Redirect to the same page to refresh the doctor list
            # return redirect('/doc')
        elif action == 'delete':
            doctor_id = int(request.form.get('doctor_id'))
            # Delete the doctor's record from the database
            res = deletedoctor(db,doctor_id)
            # Redirect to the same page to refresh the doctor list
            result = res.split()[-1]
            # return res
            if(result):
                flash('Delete successful!', 'success')
                return redirect('/doc')
                
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts) 
                flash('Delete Unsuccessful!/n'+res, 'error')
                return redirect('/doc')
