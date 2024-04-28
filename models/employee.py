from pymongo import MongoClient

def insertemployee(db, first_name, last_name, position, department_number, dob, contact_number, email, address, hire_date, salary, admin_id):
    # Access Employee collection
    employee_collection = db['Employee']
    
    # Find the last used EmployeeID, if any
    last_employee = employee_collection.find_one(sort=[("EmployeeID", -1)])

    # Determine the starting value for EmployeeID
    start_employee_id = 1 if last_employee is None else last_employee['EmployeeID'] + 1
    
    # Construct employee data
    employee_data = {
        "EmployeeID": start_employee_id,
        "AdminID": admin_id,
        "DepartmentNumber": department_number,
        "FirstName": first_name,
        "LastName": last_name,
        "Position": position,
        "DOB": dob,
        "ContactNumber": contact_number,
        "Email": email,
        "Address": address,
        "HireDate": hire_date,
        "Salary": salary,
        "AdminID": admin_id
    }
    
    # Check if the employee already exists
    existing_employee = employee_collection.find_one({"EmployeeID": start_employee_id})
    if existing_employee:
        print(f"Employee with ID {employee_id} already exists.")
        return (f"Employee with ID {employee_id} already exists.")


    # Check if the AdminID exists in the HospitalAdmin collection
    admin_exists = db['HospitalAdmin'].find_one({"AdminID": admin_id})
    if not admin_exists:
        print(f"Error: AdminID {admin_id} not found in HospitalAdmin collection for EmployeeID {employee_id}.")
        return (f"Error: AdminID {admin_id} not found in HospitalAdmin collection for EmployeeID {employee_id}.")

    # Check if the DepartmentNumber exists in the Department collection
    department_exists = db['Department'].find_one({"DepartmentNumber": department_number})
    if not department_exists:
        print(f"Error: DepartmentNumber {department_number} not found in Department collection for EmployeeID {employee_id}.")
        return (f"Error: DepartmentNumber {department_number} not found in Department collection for EmployeeID {employee_id}.")

    # Insert the data into Employee collection
    result = employee_collection.insert_one(employee_data)
    if result:
        print("Inserted ID:", result.inserted_id)
        return (f"Inserted ID: {result.inserted_id}")
    else:
        print("Failed to insert employee.")
        return (f"Failed to insert employee.")

    
def updateemployee(db, employee_id, first_name, last_name, position, department_number, dob, contact_number, email, address, hire_date, salary, admin_id):
    # Access Employee collection
    employee_collection = db['Employee']

    # Check if the employee exists
    existing_employee = employee_collection.find_one({"EmployeeID": employee_id})
    if not existing_employee:
        print(f"Employee with ID {employee_id} not found.")
        return (f"Employee with ID {employee_id} not found.")

    # Construct update query
    update_query = {}
    if admin_id:
        update_query["AdminID"] = admin_id
    if department_number:
        update_query["DepartmentNumber"] = department_number
    if first_name:
        update_query["FirstName"] = first_name
    if last_name:
        update_query["LastName"] = last_name
    if position:
        update_query["Position"] = position
    if dob:
        update_query["DOB"] = dob
    if contact_number:
        update_query["ContactNumber"] = contact_number
    if email:
        update_query["Email"] = email
    if address:
        update_query["Address"] = address
    if hire_date:
        update_query["HireDate"] = hire_date
    if salary:
        update_query["Salary"] = salary
    # Check if any update has been made
    if update_query:
        # Perform the update
        employee_collection.update_one({"EmployeeID": employee_id}, {"$set": update_query})
        print(f"Updated record for EmployeeID {employee_id}")
        return (f"Updated record for EmployeeID {employee_id}")
    else:
        print("No fields to update.")
        return ("No fields to update.")
        
        # # Perform the update
        # employee_collection.update_one({"EmployeeID": employee_id}, {"$set": update_query})
        # print(f"Updated record for EmployeeID {employee_id}")
        # return True

def deleteemployee(db, employee_id):
    # Access Employee collection
    employee_collection = db['Employee']

    # Check if the employee exists
    existing_employee = employee_collection.find_one({"EmployeeID": employee_id})
    if not existing_employee:
        print(f"Employee with ID {employee_id} not found.")
        return (f"Employee with ID {employee_id} not found.")

    # Delete the employee record
    employee_collection.delete_one({"EmployeeID": employee_id})
    print(f"Deleted record for EmployeeID {employee_id}")
    return(f"Deleted record for EmployeeID {employee_id}")

def get_employee_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    employee_collection = db['Employee']

    # Query to retrieve all doctors' records
    employee = list(employee_collection.find())

    # Close the database connection
    client.close()

    return employee