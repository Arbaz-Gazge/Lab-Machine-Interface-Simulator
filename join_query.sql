-- SQL task: Display Patient Name, Test Name, Result Value, Normal Range, Result Date, Machine Name using JOIN
SELECT 
    p.patient_name, 
    t.test_name, 
    mr.result_value, 
    t.normal_range, 
    mr.result_date, 
    mr.machine_name 
FROM Machine_Result mr
INNER JOIN Patient p ON mr.patient_id = p.patient_id
INNER JOIN Test t ON mr.test_id = t.test_id
ORDER BY mr.result_date DESC;
