#Union 
SELECT room_id, type, capacity
FROM Room
UNION ALL
SELECT bed_id, 'Bed' AS type, 1 AS capacity
FROM Bed;

SELECT room_id, type, capacity
FROM Room
WHERE room_id NOT IN (
  SELECT room_id
  FROM Bed b
  INNER JOIN Admission a ON b.room_id = room_id
  WHERE discharge_date IS NULL
)
UNION ALL
SELECT bed_id, 'Bed' AS type, 1 AS capacity
FROM Bed;

#Intersect
SELECT patient_id
FROM Admission a1
WHERE a1.doctor_id = 101
UNION
SELECT patient_id
FROM Admission a2
WHERE a2.doctor_id = 102;


SELECT 'Patients' AS type, COUNT(*) AS count
FROM Patients
UNION ALL
SELECT 'Beds' AS type, COUNT(*) AS count
FROM Bed;
