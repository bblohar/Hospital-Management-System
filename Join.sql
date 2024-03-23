#inner join 
SELECT p.patient_name, d.doctor_name, d.specialization
FROM Patients p
INNER JOIN Diagnosis diag ON p.patient_id = diag.patient_id
INNER JOIN Doctor d ON diag.doctor_id = d.doctor_id;

#Left Join 
SELECT w.ward_name, s.staff_name
FROM Ward w
LEFT JOIN Staff s ON w.staff_id = s.staff_id;

#right Join
SELECT d.doctor_name, w.ward_name
FROM Doctor d
RIGHT JOIN Ward w ON w.staff_id = d.staff_id;

SELECT p.patient_name
FROM Patients p
WHERE p.patient_id NOT IN (
  SELECT a.patient_id
  FROM Admission a
  WHERE a.doctor_id = 101
);
