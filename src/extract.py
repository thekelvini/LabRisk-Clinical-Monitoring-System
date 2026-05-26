import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/lab-results"

def extract_lab_data():
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df

    raise Exception("API extraction failed")