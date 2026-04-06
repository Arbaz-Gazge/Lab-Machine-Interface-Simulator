# Lab Machine Interface API - Quick Links

Your FastAPI application is currently running on **`http://localhost:8000`**. Below are the interactive and direct URLs to use.

---

## 1. 📂 Interactive Documentation (Recommended)
FastAPI's built-in tools allow you to test every endpoint directly from your browser.
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  
  *Best for testing POST requests.*
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 2. 🧪 API Endpoints (Quick Access)

### GET - Patient Details
Fetch core info for a specific patient.
- **URL**: [http://localhost:8000/patient/{id}](http://localhost:8000/patient/1)
- **Replace**: Replace `{id}` with a number (e.g., `1`, `6`, `101`).

### GET - Clinical Report
Fetch joined patient result data.
- **URL**: [http://localhost:8000/report/{id}](http://localhost:8000/report/1)

### GET - Machine Logs
View the last 50 simulator log entries.
- **URL**: [http://localhost:8000/machine/logs](http://localhost:8000/machine/logs)

### POST - Manual Result entry
Manually insert a result into the database.
- **URL**: `http://localhost:8000/machine/result`
- **Method**: `POST`
- **Body JSON**:
  ```json
  {
      "patient_id": 101,
      "test_id": 7,
      "result_value": "13.2",
      "machine_name": "Terminal-Manual"
  }
  ```

---

## 3. 🔍 How to Test
1. Make sure `app.py` is running (it is currently active).
2. Use **Postman**, **Insomnia**, or simply your **Web Browser** for GET requests.
3. For POST results, it is easiest to use the **Swagger UI** linked above.
