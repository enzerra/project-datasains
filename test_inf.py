import asyncio
import io
from pathlib import Path
from backend.app.config import settings
from inference_sdk import InferenceHTTPClient
import base64

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=settings.ROBOFLOW_API_KEY
)

# create dummy image
from PIL import Image
img = Image.new('RGB', (100, 100), color = 'red')
byte_io = io.BytesIO()
img.save(byte_io, 'JPEG')
b64 = base64.b64encode(byte_io.getvalue()).decode('utf-8')

print("Using PIL")
try:
    print(client.run_workflow(
        workspace_name=settings.ROBOFLOW_WORKSPACE,
        workflow_id=settings.ROBOFLOW_WORKFLOW,
        images={"image": img}
    ))
except Exception as e:
    print(e)

print("Using Base64")
try:
    print(client.run_workflow(
        workspace_name=settings.ROBOFLOW_WORKSPACE,
        workflow_id=settings.ROBOFLOW_WORKFLOW,
        images={"image": {"type": "base64", "value": b64}}
    ))
except Exception as e:
    print(e)
