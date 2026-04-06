from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from typing import List, Optional
from config import DB_CONFIG

print("""\033[96m
   ██████╗ ███████╗██╗   ██╗███████╗██╗      ██████╗ ██████╗ 
   ██╔══██╗██╔════╝██║   ██║██╔════╝██║     ██╔═══██╗██╔══██╗
   ██║  ██║█████╗  ██║   ██║█████╗  ██║     ██║   ██║██████╔╝
   ██║  ██║██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║     ██║   ██║██╔═══╝ 
   ██████╔╝███████╗ ╚████╔╝ ███████╗███████╗╚██████╔╝██║     
   ╚═════╝ ╚══════╝  ╚═══╝  ╚══════╝╚══════╝ ╚═════╝ ╚═╝     
                                                             
              \033[93m██████╗ ██╗   ██╗\033[96m
              \033[93m██╔══██╗╚██╗ ██╔╝\033[96m
              \033[93m██████╔╝ ╚████╔╝ \033[96m
              \033[93m██╔══██╗  ╚██╔╝  \033[96m
              \033[93m██████╔╝   ██║   \033[96m
              \033[93m╚═════╝    ╚═╝   \033[96m
                                                             
   \033[92m█████╗ ██████╗ ██████╗  █████╗ ███████╗ ██████╗  █████╗ ███████╗ ██████╗ ███████╗\033[0m
  \033[92m██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══███╔╝██╔════╝ ██╔══██╗╚══███╔╝██╔════╝ ██╔════╝\033[0m
  \033[92m███████║██████╔╝██████╔╝███████║  ███╔╝ ██║  ███╗███████║  ███╔╝ ██║  ███╗█████╗  \033[0m
  \033[92m██╔══██║██╔══██╗██╔══██╗██╔══██║ ███╔╝  ██║   ██║██╔══██║ ███╔╝  ██║   ██║██╔══╝  \033[0m
  \033[92m██║  ██║██║  ██║██████╔╝██║  ██║███████╗╚██████╔╝██║  ██║███████╗╚██████╔╝███████╗\033[0m
  \033[92m╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝\033[0m
\033[0m""")



app = FastAPI(title="Lab Machine Interface Simulator API")

# DB Connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Pydantic models for data
class MachineResult(BaseModel):
    patient_id: int
    test_id: int
    result_value: str
    machine_name: str

@app.get("/patient/{patient_id}")
def get_patient(patient_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed.")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Patient WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")
    
    return patient

@app.get("/report/{patient_id}")
def get_report(patient_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed.")
    
    cursor = conn.cursor(dictionary=True)
    # Perform a JOIN to get meaningful report data
    query = """
    SELECT p.patient_name, t.test_name, mr.result_value, t.normal_range, mr.result_date, mr.machine_name
    FROM Machine_Result mr
    JOIN Patient p ON mr.patient_id = p.patient_id
    JOIN Test t ON mr.test_id = t.test_id
    WHERE mr.patient_id = %s
    ORDER BY mr.result_date DESC
    """
    cursor.execute(query, (patient_id,))
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return {"patient_id": patient_id, "reports": [], "message": "No reports found for this patient."}
    
    return {"patient_id": patient_id, "reports": results}

@app.post("/machine/result")
def post_result(result: MachineResult):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed.")
    
    try:
        cursor = conn.cursor()
        # 1. Insert search Machine_Result
        cursor.execute(
            "INSERT INTO Machine_Result (patient_id, test_id, result_value, machine_name) VALUES (%s, %s, %s, %s)",
            (result.patient_id, result.test_id, result.result_value, result.machine_name)
        )
        
        # 2. Insert into Machine_Log
        cursor.execute(
            "INSERT INTO Machine_Log (message) VALUES (%s)",
            (f"Manual entry added for PatientID={result.patient_id}, TestID={result.test_id}.",)
        )
        
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Result stored successfully."}
    except mysql.connector.Error as err:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Database error: {err}")

@app.get("/machine/logs")
def get_logs():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB connection failed.")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Machine_Log ORDER BY log_time DESC LIMIT 50")
    logs = cursor.fetchall()
    conn.close()
    
    return logs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
