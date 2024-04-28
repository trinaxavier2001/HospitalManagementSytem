from pymongo import MongoClient

def insertnurse(db, employee_id, shift, qualifications):
    # Access Nurse collection
    nurse_collection = db['Nurse']

    # Check if the nurse already exists
    existing_nurse = nurse_collection.find_one({"EmployeeID": employee_id})
    if existing_nurse:
        print(f"Nurse with EmployeeID {employee_id} already exists.")
        return (f"Nurse with EmployeeID {employee_id} already exists.")
    
    # Check if EmployeeID exists in Doctor or GeneralStaff collection
    doctor_exists = db['Doctor'].find_one({"EmployeeID": employee_id})
    generalstaff_exists = db['GeneralStaff'].find_one({"EmployeeID": employee_id})
    
    if doctor_exists or generalstaff_exists:
        print(f"Error: EmployeeID {employee_id} already exists in Doctor or GeneralStaff table. Skipping insertion.")
        return(f"Error: EmployeeID {employee_id} already exists in Doctor or GeneralStaff table. Skipping insertion.")
    
    # Construct nurse data
    nurse_data = {
        "EmployeeID": employee_id,
        "Shift": shift,
        "Qualifications": qualifications
    }

    # Insert the data into Nurse collection
    result = nurse_collection.insert_one(nurse_data)
    if result:
        print("Inserted ID:", result.inserted_id)
        return (f"Inserted ID: {result.inserted_id}")
    else:
        print("Failed to insert nurse.")
        return ("Failed to insert nurse.")


def updatenurse(db, employee_id, shift, qualifications):
    # Access Nurse collection
    nurse_collection = db['Nurse']

    # Check if the nurse exists
    existing_nurse = nurse_collection.find_one({"EmployeeID": employee_id})
    if not existing_nurse:
        print(f"Nurse with EmployeeID {employee_id} not found.")
        return(f"Nurse with EmployeeID {employee_id} not found.")

    # Construct update query
    update_query = {}
    if shift:
        update_query["Shift"] = shift
    if qualifications:
        update_query["Qualifications"] = qualifications

    # Perform the update
    nurse_collection.update_one({"EmployeeID": employee_id}, {"$set": update_query})
    print(f"Updated record for EmployeeID {employee_id}")
    return (f"Updated record for EmployeeID {employee_id}")


def deletenurse(db, employee_id):
    # Access Nurse collection
    nurse_collection = db['Nurse']

    # Check if the nurse exists
    existing_nurse = nurse_collection.find_one({"EmployeeID": employee_id})
    if not existing_nurse:
        print(f"Nurse with EmployeeID {employee_id} not found.")
        return False

    # Delete the nurse record
    nurse_collection.delete_one({"EmployeeID": employee_id})
    print(f"Deleted record for EmployeeID {employee_id}")
    return True


def get_nurse_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    nurse_collection = db['Nurse']

    # Query to retrieve all doctors' records
    nurse = list(nurse_collection.find())

    # Close the database connection
    client.close()

    return nurse