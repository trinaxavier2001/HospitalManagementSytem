from flask import Flask, render_template, request, redirect, jsonify, url_for, json, flash
import csv
from pymongo import MongoClient
from datetime import datetime
from models.department import insertdepartment, updatedepartment, get_departments_records, deletedepartment


def dep_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch department records from the database
        departments = get_departments_records()

        # Render the template with the list of departments
        return render_template('/Department/Dep.html', departments=departments)
    elif request.method == 'POST':
        action = request.form.get('action')
        
        if(action == 'insertrecord'):
            return render_template('/Department/insert_department.html')

        elif(action == 'insert'):
            # Process form submission and insert data into the department table
            department_name = request.form.get("department_name")
            
            # Call the insert_department method
            res = insertdepartment(db, department_name)
            return redirect(url_for('success', message=res))
            # return redirect('/dep')
    
        elif action == 'update':
            department_number = int(request.form.get('member_id'))
            # Get the updated information for the department from the form data
            updated_department_name = request.form.get('DepartmentName')

            # Update the department's record in the database
            res = updatedepartment(db,department_number, updated_department_name)
            result = res.split()[-1]
            if result:
                flash('Update successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Update Unsuccessful!\n' + res, 'error')

        elif action == 'delete':
            department_number = int(request.form.get('member_id'))
            # Delete the department's record from the database
            res = deletedepartment(db, department_number)
            result = res.split()[-1]

            if result:
                flash('Delete successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Delete Unsuccessful!\n' + res, 'error')

    # Redirect to the same page to refresh the department list
    return redirect('/dep')
