import json
import time
from pathlib import Path
import requests

base_url = 'http://127.0.0.1:8000/api/v1'
video_path = Path(r'c:\Folder Coding\SERVER-BACKEND-MODEL\videokendaraan.mp4')

with video_path.open('rb') as f:
    upload_resp = requests.post(f'{base_url}/upload', files={'file': (video_path.name, f, 'video/mp4')}, data={'label': '', 'recorded_at': ''})
print('upload_status', upload_resp.status_code)
print(upload_resp.text)
upload_resp.raise_for_status()
upload_id = upload_resp.json()['upload_id']
print('upload_id', upload_id)

analyze_resp = requests.post(f'{base_url}/analyze', json={'upload_id': upload_id})
print('analyze_status', analyze_resp.status_code)
print(analyze_resp.text)
analyze_resp.raise_for_status()
analysis_id = analyze_resp.json()['analysis_id']
print('analysis_id', analysis_id)

for _ in range(120):
    status_resp = requests.get(f'{base_url}/status/{analysis_id}')
    print('status_status', status_resp.status_code)
    status_resp.raise_for_status()
    payload = status_resp.json()
    print('current_status', payload.get('status'), payload.get('progress', {}).get('current_step'))
    if payload.get('status') in {'completed', 'failed'}:
        print(json.dumps(payload, indent=2))
        break
    time.sleep(2)
else:
    raise SystemExit('timeout waiting for analysis')
