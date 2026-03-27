import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def debug_api(train_number):
    key = os.getenv('RAPIDAPI_KEY')
    host = os.getenv('RAPIDAPI_HOST')
    
    url = f"https://{host}/api/trains/v1/train/status"
    
    params = {
        'train_number': train_number,
        'departure_date': '20260321',
        'isH5': 'true',
        'client': 'web'
    }
    
    headers = {
        'X-RapidAPI-Key': key,
        'X-RapidAPI-Host': host
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"HTTP Status Code: {response.status_code}")
        data = response.json()
        
        with open('d:/Project_Intership/Railway_AI_System/api_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"Response saved to api_response.json for train {train_number}")
        print(f"Status: {data.get('status', 'No status')}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_api('11040')
