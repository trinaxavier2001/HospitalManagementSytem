from flask import Flask, render_template, request, redirect, jsonify, url_for, json, flash
import csv
from pymongo import MongoClient
from datetime import datetime
from models.resource_management import updateresource, deleteresource, get_resource_records

def resm_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch resource management records from the database
        resources = get_resource_records()

        # Render the template with the list of resources
        return render_template('/ResourceManagement/Resm.html', resources=resources)
    elif request.method == 'POST':
        action = request.form.get('action')
        if(action == 'insertrecord'):
            return render_template('/ResourceManagement/insert_resource_management.html')
        if action == 'update':
            resource_id = int(request.form.get('resource_id'))
            # Get the updated information for the resource from the form data
            updated_resource_type = request.form.get('resource_type')
            updated_resource_name = request.form.get('resource_name')
            updated_status = request.form.get('status')
            updated_location = request.form.get('location')
            updated_admin_id = int(request.form.get('admin_id'))

            # Update the resource's record in the database
            res = updateresource(db, resource_id, updated_resource_type, updated_resource_name, updated_status, updated_location, updated_admin_id)
            result = res.split()[-1]
            if result:
                flash('Update successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Update Unsuccessful!\n' + res, 'error')

        elif action == 'delete':
            # Delete the resource's record from the database
            resource_id = int(request.form.get('resource_id'))
            res = deleteresource(db, resource_id)
            result = res.split()[-1]

            if result:
                flash('Delete successful!', 'success')
            else:
                parts = res.split()[:-1]  # Split the string by whitespace and exclude the last element
                result = ' '.join(parts)
                flash('Delete Unsuccessful!\n' + res, 'error')

    # Redirect to the same page to refresh the resource list
    return redirect('/resm')
