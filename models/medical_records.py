# def insertmedicalrecord(db, patient_id, doctor_id, visit_date, diagnosis):
#     # Access MedicalRecords collection
#     medical_records_collection = db['MedicalRecords']
    
# #     # Find the last used EmployeeID, if any
# #     last_record = medical_records_collection.find_one(sort=[("RecordID", -1)])

# #     # Determine the starting value for EmployeeID
# #     start_record_id = 1 if last_record is None else last_record['RecordID'] + 1

#     # Construct medical record data
#     medical_record_data = {
#         "RecordID": patient_id,
#         "PatientID": patient_id,
#         "DoctorID": doctor_id,
#         "VisitDate": visit_date,
#         "Diagnosis": diagnosis
#     }

#     # Verify if DoctorID exists
#     doctor_exists = db['Doctor'].find_one({"DoctorID": doctor_id})
#     if not doctor_exists:
#         print(f"Error: DoctorID {doctor_id} does not exist. Skipping insertion for RecordID {start_record_id}.")
#         return False
    
#     # Verify if PatientID exists
#     patient_exists = db['Patient'].find_one({"PatientID": patient_id})
#     if not patient_exists:
#         print(f"Error: PatientID {patient_id} does not exist. Skipping insertion.")
#         return False
    
#     # Check if the record already exists for the same patient
#     existing_record = medical_records_collection.find_one({"RecordID": patient_id})
    
#     if existing_record:
#         # Update existing record
#         previous_visit_info = existing_record.get("VisitInfo", [])
#         previous_visit_info.append({"VisitDate": existing_record["VisitDate"], "Diagnosis": existing_record["Diagnosis"]})
        
#         # Update VisitDate, Diagnosis, and VisitInfo
#         medical_records_collection.update_one(
#             {"RecordID": existing_record["RecordID"]},
#             {"$set": {"VisitDate": visit_date, "Diagnosis": diagnosis}}
#         )
#         record_id = existing_record["RecordID"]
#         print(f"Updated record for RecordID {record_id}")
#         return True
#     else:
#         # Insert a new record
#         result = medical_records_collection.insert_one(medical_record_data)
#         if result:
#             print("Inserted ID:", result.inserted_id)
#             return True
#         else:
#             print("Failed to insert record.")
#             return False

from pymongo import MongoClient


def insertmedicalrecord(db, patient_id, doctor_id, visit_date, diagnosis):
    # Access MedicalRecords collection
    medical_records_collection = db['MedicalRecords']
    
    # Construct medical record data
    medical_record_data = {
        "RecordID": patient_id,
        "PatientID": patient_id,
        "DoctorID": doctor_id,
        "VisitDate": visit_date,
        "Diagnosis": diagnosis
    }


    # Verify if DoctorID exists
    doctor_exists = db['Doctor'].find_one({"DoctorID": doctor_id})
    

    print('doctor')
    if not doctor_exists:
        print(f"Error: DoctorID {doctor_id} does not exist. Skipping insertion.")
        return (f"Error: DoctorID {doctor_id} does not exist. Skipping insertion.")
    
    # Verify if PatientID exists
    patient_exists = db['Patient'].find_one({"PatientID": patient_id})
    if not patient_exists:
        print(f"Error: PatientID {patient_id} does not exist. Skipping insertion.")
        return (f"Error: PatientID {patient_id} does not exist. Skipping insertion.")
    
    # Check if the record already exists for the same patient
    existing_record = medical_records_collection.find_one({"RecordID": patient_id})
    
    if existing_record:
        # Update existing record
        previous_visit_info = existing_record.get("VisitInfo", [])
        previous_visit_info.append({"VisitDate": existing_record["VisitDate"], "Diagnosis": existing_record["Diagnosis"]})
        
        # Update VisitDate, Diagnosis, and VisitInfo
        medical_records_collection.update_one(
            {"RecordID": existing_record["RecordID"]},
            {"$set": {"VisitDate": visit_date, "Diagnosis": diagnosis}}
        )
        record_id = existing_record["RecordID"]
        print(f"Updated record for RecordID {record_id}")
        return (f"Updated record for RecordID {record_id}")
    else:
        # Insert a new record
        result = medical_records_collection.insert_one(medical_record_data)
        if result:
            print("Inserted ID:", result.inserted_id)
            return (f"Inserted ID:{ result.inserted_id}")
        else:
            print("Failed to insert record.")
            return (f"Failed to insert record.")


def updatemedicalrecord(db, patient_id, doctor_id, visit_date, diagnosis):
    # Access MedicalRecords collection
    medical_records_collection = db['MedicalRecords']

    # Check if the medical record exists
    existing_medical_record = medical_records_collection.find_one({"RecordID": patient_id})
    if not existing_medical_record:
        print(f"Medical record with RecordID {patient_id} not found.")
        return (f"Medical record with RecordID {patient_id} not found.")

    # Construct update query
    update_query = {}
    if patient_id:
        update_query["PatientID"] = patient_id
    if doctor_id:
        update_query["DoctorID"] = doctor_id
    if visit_date:
        update_query["VisitDate"] = visit_date
    if diagnosis:
        update_query["Diagnosis"] = diagnosis

    # Perform the update
    if update_query:
        medical_records_collection.update_one({"RecordID": patient_id}, {"$set": update_query})
        print(f"Updated record for RecordID {patient_id}")
        return (f"Updated record for RecordID {patient_id}")
    else:
        print("No fields to update.")
        return ("No fields to update.")


def deletemedicalrecord(db, record_id):
    # Access MedicalRecords collection
    medical_records_collection = db['MedicalRecords']

    # Check if the medical record exists
    existing_medical_record = medical_records_collection.find_one({"RecordID": record_id})
    if not existing_medical_record:
        print(f"Medical record with RecordID {record_id} not found.")
        return False

    # Delete the medical record
    medical_records_collection.delete_one({"RecordID": record_id})
    print(f"Deleted record for RecordID {record_id}")
    return True

def get_medical_records():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    # Access the database
    db = client['HospitalManagementSystem']
    # Access the collection containing doctors' records
    medical_records_collection = db['MedicalRecords']

    # Query to retrieve all doctors' records
    medical_records = list(medical_records_collection.find())

    # Close the database connection
    client.close()

    return medical_records