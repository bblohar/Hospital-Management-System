🏥 Sai-Samarth Hospital  (SSH)
This project implements a basic Hospital Management System, providing functionalities for receptionists, doctors, and administrators to manage patient, admission, doctor, and appointment records. It features a Flask-based backend API and a pure HTML/CSS/JavaScript frontend.

📚 Table of Contents
Features

Roles and Permissions

Technologies Used

Database Schema

Setup Instructions

Database Setup (MySQL)

Backend Setup

Frontend Setup

API Endpoints

Usage

Project Structure

Future Enhancements

Contributing

✨ Features
🔐 User Authentication: Simple login system with different roles (receptionist, doctor, admin).

👤 Patient Management:

✅ Register new patients.

✏️ Edit existing patient details.

❌ Delete patient records.

🛌 Admission Management:

➕ Record new patient admissions.

📝 Update admission details (e.g., discharge date).

🗑️ Delete admission records.

👨‍⚕️ Doctor Management:

➕ Add new doctors to the system.

✍️ Update doctor information (e.g., specialization).

🚫 Remove doctor records.

📅 Appointment Scheduling:

🗓️ Schedule new appointments for patients with doctors.

🔄 Modify existing appointment details.

✂️ Cancel appointments.

📱 Responsive UI: A clean and responsive user interface built with Tailwind CSS.

📊 Role-Based Access Control: Frontend UI elements and backend API access are controlled based on the logged-in user's role.

🧑‍💻 Roles and Permissions
The system supports the following user roles with distinct permissions:

Receptionist:

Can view and manage (add, edit, delete) patients.

Can view and manage (add, edit, delete) admissions.

Can view and manage (add, edit, delete) appointments.

Doctor:

Can view patients.

Can view admissions.

Can view and manage (add, edit, delete) their own appointments.

Admin:

Full access to all management functionalities: patients, admissions, doctors, and appointments.

Can access placeholder sections for Pharmacy, Laboratory, and Billing (UI only, no backend functionality implemented).

Login Credentials (for demonstration):

Receptionist: username: receptionist, password: pass

Doctor: username: doctor, password: pass

Admin: username: admin, password: adminpass

🛠️ Technologies Used
Backend:

🐍 Python 3

🌐 Flask: Web framework for building the RESTful API.

🔗 Flask-CORS: Enables Cross-Origin Resource Sharing.

🗄️ mysql-connector-python: Python driver for MySQL database interaction.

⏰ datetime: For handling date and time objects.

Frontend:

📄 HTML5

🎨 CSS3 (Tailwind CSS for rapid UI development)

💻 JavaScript (Vanilla JS for dynamic content and API communication)

🅰️ Google Fonts (Inter) for typography.

🗄️ Database Schema
This project is designed to work with a MySQL database. You'll need to create the necessary tables. Here's a simplified schema based on the backend code's interactions:

-- Database: sys (as configured in hms.py)

CREATE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20),
    gender CHAR(1) -- M, F, O
);

CREATE TABLE Doctor (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255),
    staff_id INT UNIQUE
);

CREATE TABLE Ward (
    ward_id INT PRIMARY KEY, -- Assuming fixed wards or managed separately
    ward_name VARCHAR(255) NOT NULL UNIQUE
);

-- Example Wards (you might want to insert these initially)
-- INSERT INTO Ward (ward_id, ward_name) VALUES (101, 'General Ward');
-- INSERT INTO Ward (ward_id, ward_name) VALUES (102, 'Pediatric Ward');
-- INSERT INTO Ward (ward_id, ward_name) VALUES (103, 'Maternity Ward');
-- INSERT INTO Ward (ward_id, ward_name) VALUES (104, 'ICU');


CREATE TABLE Admission (
    admission_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    ward_id INT NOT NULL,
    admission_date DATE NOT NULL,
    discharge_date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (ward_id) REFERENCES Ward(ward_id) ON DELETE CASCADE
);

CREATE TABLE Appointment (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id) ON DELETE CASCADE
);

⚙️ Setup Instructions
Follow these steps to get the Hospital Management System up and running on your local machine.

🗄️ Database Setup (MySQL)
Install MySQL Server: If you don't have MySQL installed, download and install it from the official MySQL website or use a package manager.

Create Database: Open your MySQL client (e.g., MySQL Workbench, command line) and create the database specified in hms.py (sys by default).

CREATE DATABASE sys;
USE sys;

Create Tables: Execute the SQL schema provided in the Database Schema section to create all necessary tables.

Configure DB_CONFIG: In hms.py, update the DB_CONFIG dictionary with your MySQL credentials:

DB_CONFIG = {
    'host': 'localhost',
    'database': 'sys', # Your database name
    'user': 'root',    # Your MySQL username
    'password': 'YourMySQLPassword' # Your MySQL password
}

Important: Replace 'YourMySQLPassword' with your actual MySQL root password or the password of the user you configured.

🖥️ Backend Setup
Clone the repository (if not already done):

git clone <your-repository-url>
cd <your-repository-name>

Navigate to the backend file:
Assuming hms.py is in the root, otherwise, adjust the path.

Create a virtual environment (recommended):

python -m venv venv

Activate the virtual environment:

On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install the required Python packages:

pip install Flask Flask-CORS mysql-connector-python

Run the Flask backend server:

python hms.py

The backend server will typically run on http://127.0.0.1:5000/. Keep this terminal window open.

🌐 Frontend Setup
The frontend is a static HTML file (hms.html). You can open it directly in your web browser.

Open hms.html:
Navigate to the hms.html file in your file explorer and open it with your preferred web browser (e.g., Chrome, Firefox).

Important: Ensure the backend server is running before opening the frontend, as the frontend will try to communicate with the backend API.

🔗 API Endpoints
The backend API provides the following endpoints under the /api prefix:

Authentication

POST /api/login: Authenticate a user and return their role.

Request Body: {"username": "...", "password": "..."}

Patients

GET /api/patients: Get all patient records.

GET /api/patients/<int:patient_id>: Get a single patient record by ID.

POST /api/patients: Add a new patient.

Request Body: {"patient_name": "...", "phone_no": "...", "gender": "..."}

PUT /api/patients/<int:patient_id>: Update an existing patient.

Request Body: {"patient_name": "...", "phone_no": "...", "gender": "..."} (send all fields)

DELETE /api/patients/<int:patient_id>: Delete a patient.

Admissions

GET /api/admissions: Get all admission records.

GET /api/admissions/<int:admission_id>: Get a single admission record by ID.

POST /api/admissions: Add a new admission.

Request Body: {"patient_id": ..., "doctor_id": ..., "ward_id": ..., "admission_date": "YYYY-MM-DD", "discharge_date": "YYYY-MM-DD"}

PUT /api/admissions/<int:admission_id>: Update an existing admission.

Request Body: {"patient_id": ..., "doctor_id": ..., "ward_id": ..., "admission_date": "YYYY-MM-DD", "discharge_date": "YYYY-MM-DD"}

DELETE /api/admissions/<int:admission_id>: Delete an admission.

Doctors

GET /api/doctors: Get all doctor records.

GET /api/doctors/<int:doctor_id>: Get a single doctor record by ID.

POST /api/doctors: Add a new doctor.

Request Body: {"doctor_name": "...", "specialization": "...", "staff_id": ...}

PUT /api/doctors/<int:doctor_id>: Update an existing doctor.

Request Body: {"doctor_name": "...", "specialization": "...", "staff_id": ...}

DELETE /api/doctors/<int:doctor_id>: Delete a doctor.

Appointments

GET /api/appointments: Get all appointment records.

GET /api/appointments/<int:appointment_id>: Get a single appointment record by ID.

POST /api/appointments: Add a new appointment.

Request Body: {"patient_id": ..., "doctor_id": ..., "appointment_date": "YYYY-MM-DD", "appointment_time": "HH:MM:SS"}

PUT /api/appointments/<int:appointment_id>: Update an existing appointment.

Request Body: {"patient_id": ..., "doctor_id": ..., "appointment_date": "YYYY-MM-DD", "appointment_time": "HH:MM:SS"}

DELETE /api/appointments/<int:appointment_id>: Delete an appointment.

🚀 Usage
Login:

Open hms.html in your browser.

Use the provided credentials to log in as a receptionist, doctor, or admin.

Navigation:

After successful login, you'll see a header with the hospital name and your role.

The main content area will display tabs based on your role (e.g., Patients, Admissions, Doctors, Appointments).

Managing Records:

Select a tab (e.g., "Patients").

Click the "Add New..." button to open a modal for creating a new record.

Fill in the form and click "Save".

Existing records will be displayed in tables. Use the "Edit" and "Delete" buttons to modify or remove records.

📂 Project Structure
.
├── hms.py            # Flask backend application for HMS
├── hms.html          # Frontend HTML, CSS, and JavaScript for HMS
└── hospital.sql      # (Assumed) SQL file for database schema and initial data

(Note: hospital.sql was not provided, but is assumed for a complete MySQL setup.)

✨ Future Enhancements
📈 Dashboard Analytics: Implement a comprehensive dashboard with key hospital metrics.

💊 Pharmacy Module: Full functionality for managing medicine inventory, prescriptions, and dispensing.

🔬 Laboratory Module: Features for ordering tests, managing results, and integrating with lab equipment.

💰 Billing & Invoicing: Comprehensive billing system, insurance integration, and payment processing.

🛌 Ward & Bed Management: Detailed tracking of ward occupancy and bed availability.

🚨 Alerts & Notifications: System for critical alerts (e.g., low stock, urgent appointments).

🔒 Enhanced Security: Implement robust authentication (e.g., JWT), authorization, and data encryption.

🧪 Automated Testing: Add unit and integration tests for both frontend and backend.

☁️ Cloud Deployment: Instructions and scripts for deploying the application to cloud platforms.

🤝 Contributing
Contributions are welcome! Please follow these steps:

🍴 Fork the repository.

🌿 Create a new branch (git checkout -b feature/your-feature-name).

✏️ Make your changes.

💾 Commit your changes (git commit -m 'Add new feature').

⬆️ Push to the branch (git push origin feature/your-feature-name).

➡️ Open a Pull Request.
