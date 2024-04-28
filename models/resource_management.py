from pymongo import MongoClient

def insertresource(db, resource_type, resource_name, status, location, admin_id):
    # Access ResourceManagement collection
    resource_management_collection = db['ResourceManagement']

    # Find the last used ResourceID, if any
    last_resource = resource_management_collection.find_one(sort=[("ResourceID", -1)])

    # Determine the starting value for ResourceID
    start_resource_id = 1 if last_resource is None else last_resource['ResourceID'] + 1


    # Construct resource data
    resource_data = {
        "ResourceID": start_resource_id,
        "ResourceType": resource_type,
        "ResourceName": resource_name,
        "Status": status,
        "Location": location,
        "AdminID": admin_id
    }
    
    # Check if the resource already exists
    existing_resource = resource_management_collection.find_one({"ResourceID": start_resource_id})
    if existing_resource:
        print(f"Resource with ResourceID {start_resource_id} already exists.")
        return False
    
    # Insert the data into ResourceManagement collection
    result = resource_management_collection.insert_one(resource_data)
    if result:
        print("Inserted ID:", result.inserted_id)
        return True
    else:
        print("Failed to insert resource.")
        return False


def updateresource(db, resource_id, resource_type, resource_name, status, location, admin_id):
    # Access ResourceManagement collection
    resource_management_collection = db['ResourceManagement']

    # Check if the resource exists
    existing_resource = resource_management_collection.find_one({"ResourceID": resource_id})
    if not existing_resource:
        print(f"Resource with ResourceID {resource_id} not found.")
        return (f"Resource with ResourceID {resource_id} not found. False")

    # Construct update query
    update_query = {}
    if resource_type:
        update_query["ResourceType"] = resource_type
    if resource_name:
        update_query["ResourceName"] = resource_name
    if status:
        update_query["Status"] = status
    if location:
        update_query["Location"] = location
    if admin_id:
        update_query["AdminID"] = admin_id

        
    # Check if any update has been made
    if update_query:
        # Perform the update
        resource_management_collection.update_one({"ResourceID": resource_id}, {"$set": update_query})
        print(f"Updated record for ResourceID {resource_id}")
        return (f"Updated record for ResourceID {resource_id} True")
    else:
        print("No fields to update.")
        return False
    # # Perform the update
    # resource_management_collection.update_one({"ResourceID": resource_id}, {"$set": update_query})
    # print(f"Updated record for ResourceID {resource_id}")
    # return True


def deleteresource(db, resource_id):
    # Access ResourceManagement collection
    resource_management_collection = db['ResourceManagement']

    # Check if the resource exists
    existing_resource = resource_management_collection.find_one({"ResourceID": resource_id})
    if not existing_resource:
        print(f"Resource with ResourceID {resource_id} not found.")
        return (f"Resource with ResourceID {resource_id} not found. False")

    # Delete the resource
    resource_management_collection.delete_one({"ResourceID": resource_id})
    print(f"Deleted record for ResourceID {resource_id}")
    return (f"Deleted record for ResourceID {resource_id} True")

def get_resource_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    resource_collection = db['ResourceManagement']

    # Query to retrieve all doctors' records
    resource = list(resource_collection.find())

    # Close the database connection
    client.close()

    return resource