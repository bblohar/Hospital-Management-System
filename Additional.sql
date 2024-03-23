SELECT p.patient_name, w.ward_name
FROM Patients p
LEFT JOIN Admission a ON p.patient_id = a.patient_id
LEFT JOIN Ward w ON a.ward_id = w.ward_id;
#left join

SELECT *
FROM Prescription p
INNER JOIN Admission a ON p.admission_id = a.admission_id
WHERE a.admission_id = 123; -- Replace 123 with actual admission ID
#inner join with on clause


SELECT p.patient_name, SUM(b.amount) AS total_bill
FROM Patients p
INNER JOIN Bill b ON b.patient_id = p.patient_id
GROUP BY p.patient_id;
#inner join with group by


