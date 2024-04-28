from flask import Flask, get_flashed_messages, render_template, request, redirect, jsonify, url_for, json, flash
import csv
from pymongo import MongoClient
from datetime import datetime
from models.general_staff import insertgeneralstaff, updategeneralstaff, get_general_staff_records, deletegeneralstaff


def gs_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch general staff records from the database
        general_staff = get_general_staff_records()

        # Render the template with the list of general staff
        return render_template('/GeneralStaff/Gen.html', general_staff=general_staff)
    elif request.method == 'POST':
        action = request.form.get('action')
        
        if(action == 'insertrecord'):
            return render_template('/GeneralStaff/insert_general_staff.html')

        elif(action == 'insert'):
            # Process form submission and insert data into the general_staff table
            employee_id = int(request.form.get("employee_id"))
            job_description = request.form.get("job_description")
            work_hours = int(request.form.get("work_hours"))
            
            # Call the insert_general_staff method
            res,success = insertgeneralstaff(db, employee_id, job_description, work_hours)
            if(success):
                flash('Insert successful!'+res, 'success')
            else:
                flash('Insert Unsuccessful!\n'+res, 'error')
            return redirect(url_for('gs',messages=res))
        
        elif action == 'update':
            employee_id = int(request.form.get('employee_id'))
            # Get the updated information for the general staff from the form data
            updated_job_description = request.form.get('job_description')
            updated_work_hours = int(request.form.get('work_hours'))

            # Update the general staff's record in the database
            res = updategeneralstaff(db, employee_id, updated_job_description, updated_work_hours)
            result = res.split()[-1]
            if result:
                flash('Update successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Update Unsuccessful!\n' + res, 'error')

        elif action == 'delete':
            employee_id = int(request.form.get('employee_id'))
            # Delete the general staff's record from the database
            res = deletegeneralstaff(db, employee_id)
            result = res.split()[-1]

            if result:
                flash('Delete successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Delete Unsuccessful!\n' + res, 'error')

    # Redirect to the same page to refresh the general staff list
    return redirect('/gs')
