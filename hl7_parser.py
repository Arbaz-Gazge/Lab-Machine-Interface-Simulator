


import mysql.connector
from config import DB_CONFIG

# HL7 Message to parse
hl7_message = """OBR|1|P101|HB|Hemoglobin\nOBX|1|NM|HB|13.2|g/dL"""

def parse_hl7_and_store(message: str):
    try:
        segments = message.strip().split('\n')
        obr = {}
        obx = {}
        
        for segment in segments:
            fields = segment.split('|')
            if fields[0] == 'OBR':
                # Example: OBR|1|P101|HB|Hemoglobin
                # Patient ID: P101 (let's assume it matches existing patient_id)
                obr['patient_id'] = fields[2].replace('P', '') # Remove 'P' prefix for ID
                obr['test_name'] = fields[4]
            elif fields[0] == 'OBX':
                # Example: OBX|1|NM|HB|13.2|g/dL
                # Result Value: 13.2
                obx['result_value'] = fields[4]
                obx['units'] = fields[5]

        print(f"Parsed Data: Patient={obr['patient_id']}, Test={obr['test_name']}, Value={obx['result_value']} {obx['units']}")

        # Store in DB
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(buffered=True)
        
        # 1. Find the test_id for 'Hemoglobin' (or the provided test name)
        cursor.execute("SELECT test_id FROM Test WHERE test_name = %s", (obr['test_name'],))
        test = cursor.fetchone()
        
        if test:
            test_id = test[0]
            # 2. Insert into Machine_Result
            cursor.execute(
                "INSERT INTO Machine_Result (patient_id, test_id, result_value, machine_name) VALUES (%s, %s, %s, %s)",
                (obr['patient_id'], test_id, f"{obx['result_value']}", "HL7-Parser-Machine")
            )
            
            # 3. Insert into Logs
            cursor.execute(
                "INSERT INTO Machine_Log (message) VALUES (%s)",
                (f"Stored HL7 machine result for patient {obr['patient_id']}, test {obr['test_name']}: {obx['result_value']}",)
            )
            
            conn.commit()
            print("Successfully stored HL7 data in database.")
        else:
            print(f"Error: Test {obr['test_name']} not found in database.")
            
        conn.close()
        
    except Exception as e:
        print(f"Error during HL7 parsing: {e}")

if __name__ == "__main__":
    parse_hl7_and_store(hl7_message)
