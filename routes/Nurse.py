from flask import Flask, render_template, request, redirect, flash
from models.nurse import updatenurse, get_nurse_records, deletenurse

def nur_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch nurse records from the database
        nurses = get_nurse_records()
 
        # Render the template with the list of nurses
        return render_template('/Nurse/Nur.html', nurses=nurses)
    
    elif request.method == 'POST':
        action = request.form.get('action')
        
        if(action == 'insertrecord'):
            return render_template('/Nurse/insert_nurse.html')
            
        elif action == 'update':
            nurse_id = int(request.form.get('employee_id'))
            # Get the updated information for the nurse from the form data
            updated_employee_id = int(request.form.get('employee_id'))
            updated_shift = request.form.get('shift')
            updated_qualification = request.form.get('qualifications')
            print(updated_employee_id,updated_shift,updated_qualification)
            # Update the nurse's record in the database
            res = updatenurse(db, updated_employee_id, updated_shift, updated_qualification)
            
            if res:
                flash('Update successful!', 'success')
            else:
                flash('Update Unsuccessful!', 'error')
 
        elif action == 'delete':
            nurse_id = int(request.form.get('employee_id'))
            # Delete the nurse's record from the database
            res = deletenurse(db, nurse_id)
            
            if res:
                flash('Delete successful!', 'success')
            else:
                flash('Delete Unsuccessful!', 'error')
 
    # Redirect to the same page to refresh the nurse list
    return redirect('/nur')
