# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS # Used to handle Cross-Origin Resource Sharing
import mysql.connector
from mysql.connector import Error
from datetime import date, time, datetime, timedelta # Import necessary datetime types

# Initialize the Flask application
app = Flask(__name__)
# Enable CORS for all routes, allowing your frontend to make requests
CORS(app)

# --- Database Configuration ---
# IMPORTANT: Replace with your actual MySQL database credentials
DB_CONFIG = {
    'host': 'localhost',
    'database': 'sys', # As per your hospital.sql file, you are using 'sys' database
    'user': '', # e.g., 'root'
    'password': '' # e.g., 'password'
}

# --- Database Connection Helper Function ---
def create_db_connection():
    """Establishes and returns a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to MySQL database")
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return connection

# --- Helper function to convert date, time, datetime, and timedelta objects to strings for JSON serialization ---
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, time):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        # Convert timedelta to string format suitable for time (HH:MM:SS)
        # This assumes timedelta represents a time of day, not a duration spanning days
        hours, remainder = divmod(obj.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
    raise TypeError ("Type %s not serializable" % type(obj))

# --- Login Endpoint (Simplified for Demonstration) ---
@app.route('/api/login', methods=['POST'])
def login():
    """
    Simulates a login process and returns a user role.
    In a real application, this would involve proper authentication
    against a user table, password hashing, and token generation.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Simple hardcoded roles for demonstration
    if username == 'receptionist' and password == 'pass':
        return jsonify({"message": "Login successful", "role": "receptionist"}), 200
    elif username == 'doctor' and password == 'pass':
        return jsonify({"message": "Login successful", "role": "doctor"}), 200
    elif username == 'admin' and password == 'adminpass':
        return jsonify({"message": "Login successful", "role": "admin"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# --- API Endpoints for Patients ---

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Fetches all patient records from the database."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True) # Use dictionary=True to get results as dicts
        cursor.execute("SELECT patient_id, patient_name, phone_no, gender FROM Patients")
        patients = cursor.fetchall()
        return jsonify(patients)
    except Error as e:
        print(f"Error fetching patients: {e}")
        return jsonify({"error": "Failed to fetch patients"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    """Fetches a single patient record by ID."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT patient_id, patient_name, phone_no, gender FROM Patients WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()
        if patient:
            return jsonify(patient)
        else:
            return jsonify({"message": "Patient not found"}), 404
    except Error as e:
        print(f"Error fetching patient: {e}")
        return jsonify({"error": "Failed to fetch patient"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/patients', methods=['POST'])
def add_patient():
    """Adds a new patient record to the database."""
    new_patient = request.json
    patient_name = new_patient.get('patient_name')
    phone_no = new_patient.get('phone_no')
    gender = new_patient.get('gender')

    if not patient_name or not gender:
        return jsonify({"error": "Patient name and gender are required"}), 400

    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        # If patient_id is provided from frontend, use it. Otherwise, rely on AUTO_INCREMENT.
        if new_patient.get('patient_id'):
            sql = "INSERT INTO Patients (patient_id, patient_name, phone_no, gender) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (new_patient['patient_id'], patient_name, phone_no, gender))
        else:
            sql = "INSERT INTO Patients (patient_name, phone_no, gender) VALUES (%s, %s, %s)"
            cursor.execute(sql, (patient_name, phone_no, gender))

        conn.commit()
        new_patient_id = new_patient.get('patient_id') if new_patient.get('patient_id') else cursor.lastrowid
        return jsonify({"message": "Patient added successfully", "patient_id": new_patient_id}), 201
    except Error as e:
        print(f"Error adding patient: {e}")
        return jsonify({"error": "Failed to add patient"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Updates an existing patient record in the database."""
    updated_data = request.json
    patient_name = updated_data.get('patient_name')
    phone_no = updated_data.get('phone_no')
    gender = updated_data.get('gender')

    if not patient_name or not gender:
        return jsonify({"error": "Patient name and gender are required"}), 400

    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = "UPDATE Patients SET patient_name = %s, phone_no = %s, gender = %s WHERE patient_id = %s"
        cursor.execute(sql, (patient_name, phone_no, gender, patient_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Patient not found"}), 404
        return jsonify({"message": "Patient updated successfully"}), 200
    except Error as e:
        print(f"Error updating patient: {e}")
        return jsonify({"error": "Failed to update patient"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Deletes a patient record from the database."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM Patients WHERE patient_id = %s"
        cursor.execute(sql, (patient_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Patient not found"}), 404
        return jsonify({"message": "Patient deleted successfully"}), 200
    except Error as e:
        print(f"Error deleting patient: {e}")
        return jsonify({"error": "Failed to delete patient"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- API Endpoints for Admissions ---

@app.route('/api/admissions', methods=['GET'])
def get_admissions():
    """Fetches all admission records with related patient, doctor, and ward names."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        # Join with Patients, Doctor, and Ward tables to get names for display
        sql = """
        SELECT
            a.admission_id,
            a.patient_id,
            p.patient_name,
            a.doctor_id,
            d.doctor_name,
            a.ward_id,
            w.ward_name,
            a.admission_date,
            a.discharge_date
        FROM Admission a
        JOIN Patients p ON a.patient_id = p.patient_id
        JOIN Doctor d ON a.doctor_id = d.doctor_id
        JOIN Ward w ON a.ward_id = w.ward_id
        """
        cursor.execute(sql)
        admissions = cursor.fetchall()
        # Convert date objects to string for JSON serialization
        for adm in admissions:
            if adm['admission_date']:
                adm['admission_date'] = json_serial(adm['admission_date'])
            if adm['discharge_date']:
                adm['discharge_date'] = json_serial(adm['discharge_date'])
        return jsonify(admissions)
    except Error as e:
        print(f"Error fetching admissions: {e}")
        return jsonify({"error": "Failed to fetch admissions"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/admissions/<int:admission_id>', methods=['GET'])
def get_admission_by_id(admission_id):
    """Fetches a single admission record by ID."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT
            a.admission_id,
            a.patient_id,
            p.patient_name,
            a.doctor_id,
            d.doctor_name,
            a.ward_id,
            w.ward_name,
            a.admission_date,
            a.discharge_date
        FROM Admission a
        JOIN Patients p ON a.patient_id = p.patient_id
        JOIN Doctor d ON a.doctor_id = d.doctor_id
        JOIN Ward w ON a.ward_id = w.ward_id
        WHERE a.admission_id = %s
        """
        cursor.execute(sql, (admission_id,))
        admission = cursor.fetchone()
        if admission:
            if admission['admission_date']:
                admission['admission_date'] = json_serial(admission['admission_date'])
            if admission['discharge_date']:
                admission['discharge_date'] = json_serial(admission['discharge_date'])
            return jsonify(admission)
        else:
            return jsonify({"message": "Admission not found"}), 404
    except Error as e:
        print(f"Error fetching admission: {e}")
        return jsonify({"error": "Failed to fetch admission"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/admissions', methods=['POST'])
def add_admission():
    """Adds a new admission record to the database."""
    new_admission = request.json
    patient_id = new_admission.get('patient_id')
    doctor_id = new_admission.get('doctor_id')
    ward_id = new_admission.get('ward_id')
    admission_date = new_admission.get('admission_date')
    discharge_date = new_admission.get('discharge_date') # Can be null

    if not all([patient_id, doctor_id, ward_id, admission_date]):
        return jsonify({"error": "Patient ID, Doctor ID, Ward ID, and Admission Date are required"}), 400

    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        # If admission_id is provided from frontend, use it. Otherwise, rely on AUTO_INCREMENT.
        if new_admission.get('admission_id'):
            sql = """
            INSERT INTO Admission (admission_id, patient_id, doctor_id, ward_id, admission_date, discharge_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (new_admission['admission_id'], patient_id, doctor_id, ward_id, admission_date, discharge_date))
        else:
            sql = """
            INSERT INTO Admission (patient_id, doctor_id, ward_id, admission_date, discharge_date)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (patient_id, doctor_id, ward_id, admission_date, discharge_date))

        conn.commit()
        new_admission_id = new_admission.get('admission_id') if new_admission.get('admission_id') else cursor.lastrowid
        return jsonify({"message": "Admission added successfully", "admission_id": new_admission_id}), 201
    except Error as e:
        print(f"Error adding admission: {e}")
        return jsonify({"error": "Failed to add admission"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/admissions/<int:admission_id>', methods=['PUT'])
def update_admission(admission_id):
    """Updates an existing admission record in the database."""
    updated_data = request.json
    patient_id = updated_data.get('patient_id')
    doctor_id = updated_data.get('doctor_id')
    ward_id = updated_data.get('ward_id')
    admission_date = updated_data.get('admission_date')
    discharge_date = updated_data.get('discharge_date')

    if not all([patient_id, doctor_id, ward_id, admission_date]):
        return jsonify({"error": "Patient ID, Doctor ID, Ward ID, and Admission Date are required"}), 400

    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE Admission
        SET patient_id = %s, doctor_id = %s, ward_id = %s, admission_date = %s, discharge_date = %s
        WHERE admission_id = %s
        """
        # CORRECTED: Ensure ward_id is included in the tuple
        cursor.execute(sql, (patient_id, doctor_id, ward_id, admission_date, discharge_date, admission_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Admission not found"}), 404
        return jsonify({"message": "Admission updated successfully"}), 200
    except Error as e:
        print(f"Error updating admission: {e}")
        return jsonify({"error": "Failed to update admission"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/admissions/<int:admission_id>', methods=['DELETE'])
def delete_admission(admission_id):
    """Deletes an admission record from the database."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM Admission WHERE admission_id = %s"
        cursor.execute(sql, (admission_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Admission not found"}), 404
        return jsonify({"message": "Admission deleted successfully"}), 200
    except Error as e:
        print(f"Error deleting admission: {e}")
        return jsonify({"error": "Failed to delete admission"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- API Endpoints for Doctors ---

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Fetches all doctor records from the database."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT doctor_id, doctor_name, specialization, staff_id FROM Doctor")
        doctors = cursor.fetchall()
        return jsonify(doctors)
    except Error as e:
        print(f"Error fetching doctors: {e}")
        return jsonify({"error": "Failed to fetch doctors"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    """Fetches a single doctor record by ID."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT doctor_id, doctor_name, specialization, staff_id FROM Doctor WHERE doctor_id = %s", (doctor_id,))
        doctor = cursor.fetchone()
        if doctor:
            return jsonify(doctor)
        else:
            return jsonify({"message": "Doctor not found"}), 404
    except Error as e:
        print(f"Error fetching doctor: {e}")
        return jsonify({"error": "Failed to fetch doctor"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/doctors', methods=['POST'])
def add_doctor():
    """Adds a new doctor record to the database."""
    new_doctor = request.json
    doctor_name = new_doctor.get('doctor_name')
    specialization = new_doctor.get('specialization')
    staff_id = new_doctor.get('staff_id')

    if not doctor_name:
        return jsonify({"error": "Doctor name is required"}), 400

    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        # If doctor_id is provided from frontend, use it. Otherwise, rely on AUTO_INCREMENT.
        if new_doctor.get('doctor_id'):
            sql = "INSERT INTO Doctor (doctor_id, doctor_name, specialization, staff_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (new_doctor['doctor_id'], doctor_name, specialization, staff_id))
        else:
            sql = "INSERT INTO Doctor (doctor_name, specialization, staff_id) VALUES (%s, %s, %s)"
            cursor.execute(sql, (doctor_name, specialization, staff_id))
        conn.commit()
        new_doctor_id = new_doctor.get('doctor_id') if new_doctor.get('doctor_id') else cursor.lastrowid
        return jsonify({"message": "Doctor added successfully", "doctor_id": new_doctor_id}), 201
    except Error as e:
        print(f"Error adding doctor: {e}")
        return jsonify({"error": "Failed to add doctor"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """Updates an existing doctor record in the database."""
    updated_data = request.json
    doctor_name = updated_data.get('doctor_name')
    specialization = updated_data.get('specialization')
    staff_id = updated_data.get('staff_id')

    if not doctor_name:
        return jsonify({"error": "Doctor name is required"}), 400

    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = "UPDATE Doctor SET doctor_name = %s, specialization = %s, staff_id = %s WHERE doctor_id = %s"
        cursor.execute(sql, (doctor_name, specialization, staff_id, doctor_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Doctor not found"}), 404
        return jsonify({"message": "Doctor updated successfully"}), 200
    except Error as e:
        print(f"Error updating doctor: {e}")
        return jsonify({"error": "Failed to update doctor"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """Deletes a doctor record from the database."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM Doctor WHERE doctor_id = %s"
        cursor.execute(sql, (doctor_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Doctor not found"}), 404
        return jsonify({"message": "Doctor deleted successfully"}), 200
    except Error as e:
        print(f"Error deleting doctor: {e}")
        return jsonify({"error": "Failed to delete doctor"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- API Endpoints for Appointments ---

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Fetches all appointment records with related patient and doctor names."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT
            ap.appointment_id,
            ap.patient_id,
            p.patient_name,
            ap.doctor_id,
            d.doctor_name,
            ap.appointment_date,
            ap.appointment_time
        FROM Appointment ap
        JOIN Patients p ON ap.patient_id = p.patient_id
        JOIN Doctor d ON ap.doctor_id = d.doctor_id
        """
        cursor.execute(sql)
        appointments = cursor.fetchall()
        # Convert date and time objects to string for JSON serialization
        for appt in appointments:
            if appt['appointment_date']:
                appt['appointment_date'] = json_serial(appt['appointment_date'])
            if appt['appointment_time']:
                appt['appointment_time'] = json_serial(appt['appointment_time']) # Apply json_serial to time objects too
        return jsonify(appointments)
    except Error as e:
        print(f"Error fetching appointments: {e}")
        if "Table 'sys.appointment' doesn't exist" in str(e):
            return jsonify({"error": "Appointments table not found. Please create it first."}), 500
        return jsonify({"error": "Failed to fetch appointments"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment_by_id(appointment_id):
    """Fetches a single appointment record by ID."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT
            ap.appointment_id,
            ap.patient_id,
            p.patient_name,
            ap.doctor_id,
            d.doctor_name,
            ap.appointment_date,
            ap.appointment_time
        FROM Appointment ap
        JOIN Patients p ON ap.patient_id = p.patient_id
        JOIN Doctor d ON ap.doctor_id = d.doctor_id
        WHERE ap.appointment_id = %s
        """
        cursor.execute(sql, (appointment_id,))
        appointment = cursor.fetchone()
        if appointment:
            if appointment['appointment_date']:
                appointment['appointment_date'] = json_serial(appointment['appointment_date'])
            if appointment['appointment_time']:
                appointment['appointment_time'] = json_serial(appointment['appointment_time'])
            return jsonify(appointment)
        else:
            return jsonify({"message": "Appointment not found"}), 404
    except Error as e:
        print(f"Error fetching appointment: {e}")
        return jsonify({"error": "Failed to fetch appointment"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/appointments', methods=['POST'])
def add_appointment():
    """Adds a new appointment record to the database."""
    new_appointment = request.json
    patient_id = new_appointment.get('patient_id')
    doctor_id = new_appointment.get('doctor_id')
    appointment_date = new_appointment.get('appointment_date')
    appointment_time = new_appointment.get('appointment_time')

    if not all([patient_id, doctor_id, appointment_date, appointment_time]):
        return jsonify({"error": "Patient ID, Doctor ID, Date, and Time are required for appointment"}), 400

    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO Appointment (patient_id, doctor_id, appointment_date, appointment_time)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (patient_id, doctor_id, appointment_date, appointment_time))
        conn.commit()
        new_appointment_id = cursor.lastrowid
        return jsonify({"message": "Appointment scheduled successfully", "appointment_id": new_appointment_id}), 201
    except Error as e:
        print(f"Error adding appointment: {e}")
        return jsonify({"error": "Failed to schedule appointment"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Updates an existing appointment record in the database."""
    updated_data = request.json
    patient_id = updated_data.get('patient_id')
    doctor_id = updated_data.get('doctor_id')
    appointment_date = updated_data.get('appointment_date')
    appointment_time = updated_data.get('appointment_time')

    if not all([patient_id, doctor_id, appointment_date, appointment_time]):
        return jsonify({"error": "Patient ID, Doctor ID, Date, and Time are required for appointment"}), 400

    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = """
        UPDATE Appointment
        SET patient_id = %s, doctor_id = %s, appointment_date = %s, appointment_time = %s
        WHERE appointment_id = %s
        """
        cursor.execute(sql, (patient_id, doctor_id, appointment_date, appointment_time, appointment_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Appointment not found"}), 404
        return jsonify({"message": "Appointment updated successfully"}), 200
    except Error as e:
        print(f"Error updating appointment: {e}")
        return jsonify({"error": "Failed to update appointment"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """Deletes an appointment record from the database."""
    conn = create_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM Appointment WHERE appointment_id = %s"
        cursor.execute(sql, (appointment_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "Appointment not found"}), 404
        return jsonify({"message": "Appointment deleted successfully"}), 200
    except Error as e:
        print(f"Error deleting appointment: {e}")
        return jsonify({"error": "Failed to delete appointment"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


# --- Main entry point for running the Flask app ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
