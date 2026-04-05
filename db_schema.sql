-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS lab_machine_db;
USE lab_machine_db;

-- Patient Table
CREATE TABLE IF NOT EXISTS Patient (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    age INT,
    gender VARCHAR(10)
);

-- Test Table
CREATE TABLE IF NOT EXISTS Test (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    test_name VARCHAR(100) NOT NULL,
    normal_range VARCHAR(50)
);

-- Machine_Result Table
CREATE TABLE IF NOT EXISTS Machine_Result (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    test_id INT,
    result_value VARCHAR(50),
    machine_name VARCHAR(100),
    result_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (test_id) REFERENCES Test(test_id) ON DELETE CASCADE
);

-- Machine_Log Table
CREATE TABLE IF NOT EXISTS Machine_Log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT,
    log_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Seed Data for Patient and Test
INSERT INTO Patient (patient_name, age, gender) VALUES 
('John Doe', 30, 'Male'),
('Jane Smith', 25, 'Female'),
('Michael Brown', 45, 'Male'),
('Emily Davis', 32, 'Female');

INSERT INTO Test (test_name, normal_range) VALUES 
('Hemoglobin', '13.5 - 17.5 g/dL'),
('Blood Sugar', '70 - 100 mg/dL'),
('WBC Count', '4500 - 11000 cells/mcL'),
('Cholesterol', '< 200 mg/dL');
