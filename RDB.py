from datetime import datetime
from flask import Flask, jsonify, render_template, request
import pyodbc

app = Flask(__name__)

# Database connection parameters
server = 'DESKTOP-QN4PIM3'
database = 'HospitalManagementSystem'
# username = 'supre'
# password = 'supre'

# For Windows Authentication, specify Trusted_Connection=yes and remove the username and password
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
# # Create a connection string
# connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
# Function to establish database connection
def get_connection():
    return pyodbc.connect(connection_string)

# Close the database connection when the application context is destroyed
@app.teardown_appcontext
def teardown_db_connection(exception):
    conn = get_connection()
    if conn is not None:
        conn.close()

# Route to render the index page
@app.route('/index1')
def index():
    try:
        # Get database connection from application context
        conn = get_connection()

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Example query to fetch appointment data
        query = "SELECT * FROM Appointment"

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        appointments = cursor.fetchall()

        # Close the cursor (don't close the connection)
        cursor.close()

        # Render the appointments.html template with the list of appointments
        return render_template('Appointment/Appo2.html', appointments=appointments)

    except pyodbc.Error as e:
        return f"Error connecting to database: {e}"

# Route to fetch appointments
@app.route('/appo2')
def get_appointments():
    try:
        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Example query to fetch appointment data
        query = "SELECT * FROM Appointment"

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        appointments = cursor.fetchall()

        # Convert results to a list of dictionaries
        appointment_list = []
        for appointment in appointments:
            appointment_dict = {
                'AppointmentID': appointment[0],
                'PatientID': appointment[1],
                'DepartmentNumber': appointment[2],
                'DateTime': appointment[3],
                'Purpose': appointment[4],
                'Status': appointment[5]
            }
            appointment_list.append(appointment_dict)

        # Close the cursor and connection
        cursor.close()
        conn.close()
        return render_template('Appointment/Appo2.html', appointments=appointments)
        # Return appointment data as JSON
        # return jsonify(appointment_list)

    except pyodbc.Error as e:
        return f"Error fetching appointments: {e}"



# Function to fetch appointment record by ID from MSSQL
def get_appointment_record(appointment_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Appointment WHERE AppointmentID=?", appointment_id)
            appointment = cursor.fetchone()
            cursor.close()
            conn.close()
            if appointment:
                return {
                    'AppointmentID': appointment[0],
                    'PatientID': appointment[1],
                    'DoctorID': appointment[2],
                    'DateTime': appointment[3],
                    'Purpose': appointment[4],
                    'Status': appointment[5]
                }
            else:
                return None
        except Exception as e:
            print("Fetch Error: ", e)
            return None
    else:
        return None

# Function to update appointment record in MSSQL
def update_appointment_record(appointment_id, updated_patient_id, updated_doctor_id, updated_datetime, updated_purpose, updated_status):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Appointment SET PatientID=?, DepartmentNumber=?, DateTime=?, Purpose=?, Status=? WHERE AppointmentID=?", 
                           updated_patient_id, updated_doctor_id, updated_datetime, updated_purpose, updated_status, appointment_id)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Update Error: ", e)
            return False
    else:
        return False

# Function to delete appointment record from MSSQL
def delete_appointment_record(appointment_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Appointment WHERE AppointmentID=?", appointment_id)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Delete Error: ", e)
            return False
    else:
        return False
    
# Flask route to handle GET and PUT requests for a specific appointment ID
@app.route('/appo/<int:appointment_id>', methods=['GET', 'PUT'])
def handle_appointment(appointment_id):
    print(request.method)
    if request.method == 'GET':
        appointment = get_appointment_record(appointment_id)
        print(appointment)
        if appointment:
            return jsonify(appointment), 200
        else:
            return jsonify({"error": "Appointment not found"}), 404
    elif request.method == 'PUT':
        print('entered')
        updated_data = request.json
        action = updated_data.get('action')
        if action == 'update':
            updated_patient_id = updated_data.get('PatientID')
            updated_doctor_id = updated_data.get('DoctorID')
            updated_datetime = updated_data.get('DateTime')
            date_time_obj = datetime.strptime(updated_datetime, '%Y-%m-%dT%H:%M')
            # Format the datetime object into the desired format
            formatted_date_time_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
            updated_purpose = updated_data.get('Purpose')
            updated_status = updated_data.get('Status')
            success = update_appointment_record(appointment_id, updated_patient_id, updated_doctor_id, formatted_date_time_str, updated_purpose, updated_status)
            if success:
                appointments = get_appointment_record(appointment_id)
                return render_template('Appointment/Appo2.html', appointments=appointments)
            else:
                return jsonify({"error": "Failed to update appointment"}), 500
        elif action == 'delete':
            success = delete_appointment_record(appointment_id)
            if success:
                appointments = get_appointment_record()
                return render_template('/Appointment/Appo1.html', appointments=appointments)
            else:
                return jsonify({"error": "Failed to delete appointment"}), 500

@app.route('/appo', methods=['GET'])
def edit_appointment():
    return render_template('Appointment/Appo2edit.html')

if __name__ == '__main__':
    app.run(debug=True)
