from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['HospitalManagementSystem']
def insertdoctor(db, employee_id, specialization):
    # Access Doctor collection
    doctor_collection = db['Doctor']
     
    # Find the last used DoctorID, if any
    last_doctor = doctor_collection.find_one(sort=[("DoctorID", -1)])

    # Determine the starting value for DoctorID
    start_doctor_id = 1 if last_doctor is None else last_doctor['DoctorID'] + 1

    # Initialize doctor_id with start_doctor_id
    doctor_id = start_doctor_id
    
    # Check if the doctor already exists
    existing_doctor = doctor_collection.find_one({"DoctorID": doctor_id})
    if existing_doctor:
        print(f"Doctor with ID {doctor_id} already exists.")
        return (f"Doctor with ID {doctor_id} already exists.")
     
    # Check if EmployeeID exists in Doctor or GeneralStaff collection
    general_staff_exists = db['GeneralStaff'].find_one({"EmployeeID": employee_id})
    nurse_exists = db['Nurse'].find_one({"EmployeeID": employee_id})
    employee_exists = db['Employee'].find_one({"EmployeeID": employee_id})
    
    if not employee_exists:
        return((f"Error: EmployeeID {employee_id} does not exist in Employee table. Skipping insertion."))

    if general_staff_exists or nurse_exists or employee_exists:
        return(f"Error: EmployeeID {employee_id} already exists in Nurse or GeneralStaff table. Skipping insertion.")
    
    # Construct doctor data
    doctor_data = {
        "DoctorID": doctor_id,
        "EmployeeID": employee_id,
        "Specialization": specialization
    }
    
    # Insert the data into Doctor collection with existing or auto-incremented DoctorID
    doctor_id = existing_doctor['DoctorID'] if existing_doctor else start_doctor_id
    doctor_data["DoctorID"] = doctor_id    
    result = doctor_collection.insert_one(doctor_data)
    
    if result:
        print("Inserted ID:", result.inserted_id)
        return (f"Inserted ID: {result.inserted_id}")
    else:
        print("Failed to insert doctor.")
        return ("Failed to insert doctor False")


def updatedoctor(db, doctor_id, employee_id, specialization):
    # Access Doctor collection
    doctor_collection = db['Doctor']

    # Check if the doctor exists
    existing_doctor = doctor_collection.find_one({"DoctorID": doctor_id})
    if not existing_doctor:
        print(f"Doctor with ID {doctor_id} not found.")
        return(f"Doctor with ID {doctor_id, employee_id, specialization} not found False")

    # Check if the provided employee ID matches the DoctorID
    if existing_doctor['EmployeeID'] != employee_id:
        print(f"Employee ID {employee_id} does not match DoctorID {doctor_id}.")
        return(f"Employee ID {employee_id} does not match DoctorID {doctor_id} False")

    # Construct update query
    update_query = {}
    if employee_id:
        update_query["EmployeeID"] = employee_id
    if specialization:
        update_query["Specialization"] = specialization

    # Perform the update
    doctor_collection.update_one({"DoctorID": doctor_id}, {"$set": update_query})
    print(f"Updated record for DoctorID {doctor_id}")
    return (f"Updated record for DoctorID {doctor_id} True")



def deletedoctor(db, doctor_id):
    # Access Doctor collection
    doctor_collection = db['Doctor']

    # Check if the doctor exists
    existing_doctor = doctor_collection.find_one({"DoctorID": doctor_id})
    if not existing_doctor:
        print(f"Doctor with ID {doctor_id} not found.")
        return (f"Doctor with ID {doctor_id} not found. False")

    # Delete the doctor record
    doctor_collection.delete_one({"DoctorID": doctor_id})
    print(f"Deleted record for DoctorID {doctor_id}")
    return (f"Deleted record for DoctorID {doctor_id} True")

def get_doctors_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    doctors_collection = db['Doctor']

    # Query to retrieve all doctors' records
    doctors = list(doctors_collection.find())

    # Close the database connection
    client.close()

    return doctors