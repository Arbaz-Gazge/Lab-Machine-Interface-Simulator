# Debugging Scenario: Machine results inserted, but reports not visible in API.

### Problem Analysis
If machine results are confirmed to be in the database (e.g., using a SQL client) but are not appearing in the API response, there are several possible causes.

### Step-by-Step Debugging & Fixes

1.  **Verify Data Completeness (Foreign Keys)**:
    -   **Issue**: Results might be inserted with invalid `patient_id` or `test_id` if foreign key constraints are not enforced or if the simulator is using IDs that don't exist in the `Patient` or `Test` tables.
    -   **Debug**: Check the `Machine_Result` table for nulls or mismatched IDs.
    -   **Fix**: Ensure the simulator fetches valid IDs from the database before insertion.

2.  **API Join Condition Logic**:
    -   **Issue**: The `JOIN` query in the API might be using an `INNER JOIN` on a table that is empty or has mismatched values. For example, if a `test_id` is missing in the `Test` table, `INNER JOIN` will exclude that row from results.
    -   **Debug**: Run the JOIN query manually in a MySQL client.
    -   **Fix**: If some data might be missing, use `LEFT JOIN` to see results even if related table data is absent.

3.  **Database Connection Mismatch**:
    -   **Issue**: The machine simulator and the API might be connecting to different databases or different host environments (e.g., local vs production).
    -   **Debug**: Print the database name and host in both applications at startup.
    -   **Fix**: Align the `DB_CONFIG` in both scripts.

4.  **Data Caching (API or Client-side)**:
    -   **Issue**: The API or the frontend might be caching GET requests, showing stale empty results.
    -   **Debug**: Use tools like Postman or `curl` to call the API directly and check headers for cache control.
    -   **Fix**: Disable caching or add `no-cache` headers to the API response.

5.  **Data Type Mismatch or Query Filtering**:
    -   **Issue**: The API might be filtering by `patient_id` using a different type (e.g., string vs integer) or applying a filter (like `WHERE result_date > TODAY`) that excludes recent inputs.
    -   **Debug**: Log the exact SQL query being executed by the API.
    -   **Fix**: Correct the WHERE clause or data type handling in the API.

6.  **Transaction Commit Issue**:
    -   **Issue**: The machine simulator might be inserting data but forgetting to call `conn.commit()`. While the simulator's session might see the data, other sessions (like the API) will not.
    -   **Debug**: Check if data persists after restarting the simulator.
    -   **Fix**: Ensure `conn.commit()` is called after every INSERT in the simulator.
