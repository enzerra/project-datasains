import requests
import time
import json
import sys

base_url = 'http://127.0.0.1:8000/api/v1'
video_path = r'C:/Folder Coding/SERVER-BACKEND-MODEL/videokendaraan.mp4'

try:
    print(f'Uploading {video_path}...')
    with open(video_path, 'rb') as f:
        response = requests.post(f'{base_url}/upload', files={'file': f})
    response.raise_for_status()
    upload_id = response.json()['upload_id']
    print(f'Upload successful. upload_id: {upload_id}')

    print('Starting analysis...')
    response = requests.post(f'{base_url}/analyze', json={'upload_id': upload_id})
    response.raise_for_status()
    analysis_id = response.json()['analysis_id']
    print(f'Analysis started. analysis_id: {analysis_id}')

    while True:
        response = requests.get(f'{base_url}/status/{analysis_id}')
        response.raise_for_status()
        data = response.json()
        status = data.get('status')
        print(f'Status: {status}')

        if status == 'completed':
            result = data.get('result', {})
            print("\nFinal Result:")
            print(json.dumps(result, indent=2))
            break
        elif status == 'failed':
            print(f"\nAnalysis failed: {data.get('error')}")
            sys.exit(1)
        
        time.sleep(2)

except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
