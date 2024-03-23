use sys;
CREATE TABLE Patients (
  patient_id INT PRIMARY KEY,
  patient_name VARCHAR(255) NOT NULL,
  phone_no VARCHAR(20),
  gender varchar(2)
);

CREATE TABLE Staff (
  staff_id INT PRIMARY KEY,
  staff_name VARCHAR(255) ,
  department_id INT
);

CREATE TABLE Department (
  department_id INT PRIMARY KEY,
  department_name VARCHAR(255) 
);

CREATE TABLE Ward (
  ward_id INT PRIMARY KEY,
  ward_name VARCHAR(255) NOT NULL,
  capacity INT,
  staff_id INT (20)
);

CREATE TABLE Room (
  room_id INT PRIMARY KEY,
  type VARCHAR(255) NOT NULL,
  capacity INT,
  ward_id INT (20)
);

CREATE TABLE Bed (
  bed_id INT PRIMARY KEY,
  room_id INT (20)
);

CREATE TABLE Doctor (
  doctor_id INT PRIMARY KEY,
  doctor_name VARCHAR(255) NOT NULL,
  specialization VARCHAR(255),
  staff_id INT (20)
);

CREATE TABLE Diagnosis (
  diagnosis_id INT PRIMARY KEY,
  patient_id INT (20),
  doctor_id INT (20)
);

CREATE TABLE Admission (
  admission_id INT PRIMARY KEY,
  patient_id INT (20),
  doctor_id INT (20),
  ward_id INT (20),
  admission_date DATE,
  discharge_date DATE
);

CREATE TABLE Prescription (
  prescription_id INT PRIMARY KEY,
  admission_id INT (20),
  doctor_id INT (20),
  patient_name VARCHAR(255),
  medication_name VARCHAR(255),
  dosage VARCHAR(255)
);

CREATE TABLE Test (
  test_id INT PRIMARY KEY,
  test_name VARCHAR(255) NOT NULL
);

CREATE TABLE Test_Results (
  test_result_id INT PRIMARY KEY,
  admission_id INT (20),
  test_id INT (20),
  result VARCHAR(255)
);

CREATE TABLE Bill (
  bill_id INT PRIMARY KEY,
  patient_id INT (20),
  room_id INT (20),
  pay_date DATE,
  amount DECIMAL(10,2)
);
