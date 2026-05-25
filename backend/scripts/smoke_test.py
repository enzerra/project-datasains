import json
import time
import urllib.request
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
file_path = Path(__file__).resolve().parents[1] / "tmp" / "test.jpg"

boundary = "----boundary"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
    "Content-Type: image/jpeg\r\n\r\n"
).encode() + file_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()

upload_req = urllib.request.Request(
    f"{BASE_URL}/api/v1/upload",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    method="POST",
)
upload = json.loads(urllib.request.urlopen(upload_req).read().decode())
print("upload", upload)

analyze_req = urllib.request.Request(
    f"{BASE_URL}/api/v1/analyze",
    data=json.dumps({"upload_id": upload["upload_id"]}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
analyze = json.loads(urllib.request.urlopen(analyze_req).read().decode())
print("analyze", analyze)

analysis_id = analyze["analysis_id"]
for _ in range(30):
    status = json.loads(urllib.request.urlopen(f"{BASE_URL}/api/v1/status/{analysis_id}").read().decode())
    print("status", status["status"], (status.get("progress") or {}).get("message"))
    if status["status"] in ("completed", "failed"):
        print(json.dumps(status, indent=2)[:1500])
        break
    time.sleep(2)
