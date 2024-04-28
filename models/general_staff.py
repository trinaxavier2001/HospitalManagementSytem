from pymongo import MongoClient

def insertgeneralstaff(db, employee_id, job_description, work_hours):
    # Access GeneralStaff collection
    general_staff_collection = db['GeneralStaff']

    # Check if the general staff already exists
    existing_general_staff = general_staff_collection.find_one({"EmployeeID": employee_id})
    if existing_general_staff:
        return (f"General staff with EmployeeID {employee_id} already exists.",True)
    # Check if EmployeeID exists in Doctor or GeneralStaff collection
    doctor_exists = db['Doctor'].find_one({"EmployeeID": employee_id})
    nurse_exists = db['Nurse'].find_one({"EmployeeID": employee_id})
    
    if doctor_exists or nurse_exists:
        return(f"Error: EmployeeID {employee_id} already exists in Doctor or GeneralStaff table. Skipping insertion.", False)
    
    # Construct general staff data
    general_staff_data = {
        "EmployeeID": employee_id,
        "JobDescription": job_description,
        "WorkHours": work_hours
    }

    # Insert the data into GeneralStaff collection
    result = general_staff_collection.insert_one(general_staff_data)
    if result:
        print("Inserted ID:", result.inserted_id)
        return (f"Inserted ID: {result.inserted_id}",True)
    else:
        print("Failed to insert general staff.")
        return (f"Failed to insert general staff.", False)


def updategeneralstaff(db, employee_id, job_description, work_hours):
    # Access GeneralStaff collection
    general_staff_collection = db['GeneralStaff']

    # Check if the general staff exists
    existing_general_staff = general_staff_collection.find_one({"EmployeeID": employee_id})
    if not existing_general_staff:
        print(f"General staff with EmployeeID {employee_id} not found. False")
        return (f"General staff with EmployeeID {employee_id} not found. False")

    # Construct update query
    update_query = {}
    if job_description:
        update_query["JobDescription"] = job_description
    if work_hours:
        update_query["WorkHours"] = work_hours

    # Perform the update
    general_staff_collection.update_one({"EmployeeID": employee_id}, {"$set": update_query})
    print(f"Updated record for EmployeeID {employee_id} True")
    return (f"Updated record for EmployeeID {employee_id} True")


def deletegeneralstaff(db, employee_id):
    # Access GeneralStaff collection
    general_staff_collection = db['GeneralStaff']

    # Check if the general staff exists
    existing_general_staff = general_staff_collection.find_one({"EmployeeID": employee_id})
    if not existing_general_staff:
        print(f"General staff with EmployeeID {employee_id} not found. False")
        return False

    # Delete the general staff record
    general_staff_collection.delete_one({"EmployeeID": employee_id})
    print(f"Deleted record for EmployeeID {employee_id} True")
    return (f"Deleted record for EmployeeID {employee_id} True")


def get_general_staff_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    general_staff_collection = db['GeneralStaff']

    # Query to retrieve all doctors' records
    general_staff = list(general_staff_collection.find())

    # Close the database connection
    client.close()

    return general_staff