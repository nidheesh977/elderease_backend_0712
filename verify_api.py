import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("Waiting for server to start...")
    time.sleep(5)
    
    # 1. Create Patient
    print("\n1. Testing Create Patient...")
    patient_data = {
        "name": "John Doe",
        "age": 75,
        "gender": "Male",
        "chief_complaint": "Hypertension"
    }
    response = requests.post(f"{BASE_URL}/patients", json=patient_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 201:
        patient_id = response.json()['id']
    else:
        print("Failed to create patient")
        return

    # 2. Get Patient Detail
    print(f"\n2. Testing Get Patient Detail (ID: {patient_id})...")
    response = requests.get(f"{BASE_URL}/patients/{patient_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    # 3. Add Daily Record
    print("\n3. Testing Add Daily Record...")
    record_data = {
        "patient_id": patient_id,
        "weight": 70.5,
        "bp": "120/80",
        "notes": "Feeling good"
    }
    response = requests.post(f"{BASE_URL}/daily/record", json=record_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    # 4. Get Dashboard
    print("\n4. Testing Dashboard...")
    response = requests.get(f"{BASE_URL}/home/dashboard")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"Error: {e}")
