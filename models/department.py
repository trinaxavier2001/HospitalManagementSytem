from pymongo import MongoClient

def insertdepartment(db, department_name):
    # Access Department collection
    department_collection = db['Department']
    
    # Find the last used DepartmentNumber, if any
    last_department = department_collection.find_one(sort=[("DepartmentNumber", -1)])

    # Determine the starting value for DepartmentNumber
    start_department_number = 1 if last_department is None else last_department['DepartmentNumber'] + 1
    
    # Check if the department already exists
    existing_department = department_collection.find_one({
        "$or": [
            {"DepartmentNumber": start_department_number},
            {"DepartmentName": department_name}
        ]
    })

    if existing_department:
        return (f"Department with DepartmentNumber {start_department_number} or DepartmentName {department_name} already exists.")

    # Construct department data
    department_data = {
        "DepartmentNumber": start_department_number,
        "DepartmentName": department_name
    }

    # Insert the data into Department collection
    result = department_collection.insert_one(department_data)
    if result:
        print("Inserted ID:", result.inserted_id)
        return (f"Inserted ID: {result.inserted_id}")
    else:
        print("Failed to insert department.")
        return ("Failed to insert department.")


def updatedepartment(db, department_number, department_name):
    # Access Department collection
    department_collection = db['Department']

    # Check if the department exists
    existing_department_number = department_collection.find_one({"DepartmentNumber": department_number})
        
    existing_department_name = department_collection.find_one({"DepartmentName": department_name})

    if existing_department_number:
        if existing_department_name:
            return (f"Department with DepartmentName {department_name} already exists. False" )
    else:
        return (f"Department with DepartmentNumber {department_number} already exists. False")
    
    if existing_department_number:
        # Construct update query
        update_query = {}
        if department_name:
            update_query["DepartmentName"] = department_name

        # Perform the update
        department_collection.update_one({"DepartmentNumber": department_number}, {"$set": update_query})
        print(f"Updated record for DepartmentNumber {department_number}")
        return (f"Updated record for DepartmentNumber {department_number},{department_name} True")


def deletedepartment(db, department_number):
    # Access Department collection
    department_collection = db['Department']

    # Check if the department exists
    existing_department = department_collection.find_one({"DepartmentNumber": department_number})
    if not existing_department:
        print(f"Department with DepartmentNumber {department_number} not found. False")
        return (f"Department with DepartmentNumber {department_number} not found. False")

    # Delete the department
    department_collection.delete_one({"DepartmentNumber": department_number})
    print(f"Deleted record for DepartmentNumber {department_number}")
    return (f"Deleted record for DepartmentNumber {department_number} True")

def get_departments_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    departments_collection = db['Department']

    # Query to retrieve all doctors' records
    departments = list(departments_collection.find())

    # Close the database connection
    client.close()

    return departments