#count
SELECT COUNT(*) AS total_patients
FROM Patients;

#average 
SELECT AVG(capacity) AS avg_ward_capacity
FROM Ward;

SELECT medication_name, COUNT(*) AS frequency
FROM Prescription
GROUP BY medication_name
ORDER BY frequency DESC
LIMIT 1;

#sum 
SELECT p.patient_name, SUM(b.amount) AS total_bill
FROM Patients p
INNER JOIN Bill b ON p.patient_id = b.patient_id
GROUP BY p.patient_id;

SELECT d.doctor_name, COUNT(a.admission_id) AS patient_count
FROM Doctor d
INNER JOIN Admission a ON d.doctor_id = a.doctor_id
WHERE a.admission_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY d.doctor_id;

#average
SELECT w.ward_name, AVG(b.amount) AS avg_ward_bill
FROM Ward w
INNER JOIN Room r ON w.ward_id = r.ward_id
INNER JOIN Bill b ON r.room_id = b.room_id
GROUP BY w.ward_id
ORDER BY avg_ward_bill DESC
LIMIT 1;

