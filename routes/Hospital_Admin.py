from flask import Flask, render_template, request, redirect, jsonify, url_for, json, flash
import csv
from pymongo import MongoClient
from datetime import datetime
from models.hospital_admin import inserthospitaladmin, updatehospitaladmin, get_hospital_admin_records, deletehospitaladmin


def ha_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch hospital admin records from the database
        hospital_admins = get_hospital_admin_records()

        # Render the template with the list of hospital admins
        return render_template('/HospitalAdmin/Hos.html', hospital_admins=hospital_admins)
    elif request.method == 'POST':
        action = request.form.get('action')
        if(action == 'insertrecord'):
            return render_template('/HospitalAdmin/insert_hospital_admin.html')

        elif(action == 'insert'):
            # Process form submission and insert data into the hospital admin table
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            contact_number = request.form.get("contact_number")
            email = request.form.get("email")
            address = request.form.get("address")
            role = request.form.get("role")
        
            res,success = inserthospitaladmin(db, first_name, last_name, contact_number, email, address, role)
            if success:
                flash(f'Insert Successful!\n {res}', 'success')
                return redirect(url_for('ha', messages=res))
            else:
                flash(f'Insert Unuccessful!', 'error')
                return redirect(url_for('ha', messages=res))
            # return redirect('/dep')
        
        if action == 'update':
            admin_id = int(request.form.get('admin_id'))

            # Get the updated information for the hospital admin from the form data
            updated_first_name = request.form.get('first_name')
            updated_last_name = request.form.get('last_name')
            updated_contact_number = int(request.form.get('contact_number'))
            updated_email = request.form.get('email')
            updated_address = request.form.get('address')
            updated_role = request.form.get('role')

            # Update the hospital admin's record in the database
            res = updatehospitaladmin(db, admin_id, updated_first_name, updated_last_name, updated_contact_number, updated_email, updated_address, updated_role)
            result = res.split()[-1]
            if result:
                flash('Update successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Update Unsuccessful!\n' + res, 'error')

        elif action == 'delete':
            admin_id = int(request.form.get('admin_id'))

            # Delete the hospital admin's record from the database
            res = deletehospitaladmin(db, admin_id)
            result = res.split()[-1]

            if result:
                flash('Delete successful!', 'success')
                return redirect(url_for('ha', messages=res))
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Delete Unsuccessful!\n' + res, 'error')
                return redirect(url_for('ha', messages=res))

    # Redirect to the same page to refresh the hospital admin list
    return redirect('/ha')
