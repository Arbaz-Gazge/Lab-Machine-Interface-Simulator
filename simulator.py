import time
import random
import mysql.connector
from config import DB_CONFIG

# Connect to the MySQL database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def run_simulator():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database. Simulator stopped.")
        return

    cursor = conn.cursor(dictionary=True)
    
    while True:
        try:
            # 1. Fetch random patient
            cursor.execute("SELECT patient_id FROM Patient ORDER BY RAND() LIMIT 1")
            patient = cursor.fetchone()
            
            # 2. Fetch random test
            cursor.execute("SELECT test_id, test_name FROM Test ORDER BY RAND() LIMIT 1")
            test = cursor.fetchone()
            
            if patient and test:
                patient_id = patient['patient_id']
                test_id = test['test_id']
                test_name = test['test_name']
                
                # 3. Generate random result value (e.g., hemoglobin or blood sugar)
                if test_name == 'Hemoglobin':
                    result_value = f"{round(random.uniform(10, 18), 1)}" # 10.0 - 18.0 g/dL
                elif test_name == 'Blood Sugar':
                    result_value = f"{random.randint(60, 200)}" # 60 - 200 mg/dL
                else:
                    result_value = f"{random.randint(100, 5000)}" # Generic value
                
                machine_name = "ABC-Analyzer-X100"
                
                # 4. Insert data into Machine_Result
                cursor.execute(
                    "INSERT INTO Machine_Result (patient_id, test_id, result_value, machine_name) VALUES (%s, %s, %s, %s)",
                    (patient_id, test_id, result_value, machine_name)
                )
                
                # 5. Insert logs into Machine_Log
                cursor.execute(
                    "INSERT INTO Machine_Log (message) VALUES (%s)",
                    (f"Stored machine result for patient {patient_id}, test {test_id}: {result_value}",)
                )
                
                conn.commit()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Result inserted: PatientID={patient_id}, TestID={test_id}, Value={result_value}")
            else:
                print("Patient or Test table is empty. Please seed data first.")
                break
                
        except mysql.connector.Error as err:
            print(f"Error during simulation: {err}")
            
        time.sleep(10)

if __name__ == "__main__":
    run_simulator()
