from flask import Flask, render_template, request, redirect, flash
from models.employee import updateemployee, get_employee_records, deleteemployee

def emp_record(db):
    if request.method == 'GET':
        # Assuming you have a function to fetch employee records from the database
        employees = get_employee_records()
 
        # Render the template with the list of employees
        return render_template('/Employee/Emp.html', employees=employees)
    
    elif request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'insertrecord':
            return render_template('/Employee/insert_employee.html')
            
        elif action == 'update':
            employee_id = int(request.form.get('employee_id'))
            # Get the updated information for the employee from the form data
            updated_first_name = request.form.get('first_name')
            updated_last_name = request.form.get('last_name')
            updated_position = request.form.get('position')
            updated_department_number = request.form.get('department_number')
            updated_date_of_birth = request.form.get('date_of_birth')
            updated_contact_number = request.form.get('contact_number')
            updated_email = request.form.get('email')
            updated_address = request.form.get('address')
            updated_hire_date = request.form.get('hire_date')
            updated_salary = request.form.get('salary')
            updated_admin_id = request.form.get('admin_id')
            print(updated_first_name, updated_last_name, updated_position, updated_department_number, updated_date_of_birth, updated_contact_number, updated_email, updated_address, updated_hire_date, updated_salary, updated_admin_id)
            # Update the employee's record in the database
            res = updateemployee(db, employee_id, updated_first_name, updated_last_name, updated_position, updated_department_number, updated_date_of_birth, updated_contact_number, updated_email, updated_address, updated_hire_date, updated_salary, updated_admin_id)
            
            if res:
                flash('Update successful!', 'success')
            else:
                flash('Update Unsuccessful!', 'error')
 
        elif action == 'delete':
            employee_id = int(request.form.get('employee_id'))
            # Delete the employee's record from the database
            res = deleteemployee(db, employee_id)
            
            if res:
                flash('Delete successful!', 'success')
            else:
                flash('Delete Unsuccessful!', 'error')
 
    # Redirect to the same page to refresh the employee list
    return redirect('/emp')
