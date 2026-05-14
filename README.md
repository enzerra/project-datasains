# Traffic Congestion Predictor

Full-stack traffic congestion analysis app using Next.js 14 and FastAPI.

## Roboflow env

If you are using the Inference SDK style shown in the prompt, set:

- `ROBOFLOW_API_URL=https://serverless.roboflow.com`
- `ROBOFLOW_PROJECT_ID=my-traffic-congestion`
- `ROBOFLOW_MODEL_VERSION=1`

Keep `ROBOFLOW_WORKSPACE` and `ROBOFLOW_WORKFLOW_ID` only if you later switch the backend to the Workflow API path.

## Structure

- `frontend/` - Next.js app router frontend
- `backend/` - FastAPI middleware and Roboflow integration
- `docs/` - setup and architecture notes

## Quick start

1. Copy environment files in `frontend/` and `backend/`.
2. Install backend and frontend dependencies.
3. Start the backend on port `8000`.
4. Start the frontend on port `3000`.

## Deploy without Docker

### Backend (Railway)

1. Create a new Railway project from this GitHub repository.
2. Set the service root directory to `backend`.
3. Railway will use `backend/Procfile` automatically with this command:
	- `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`
4. Add these Railway environment variables:
	- `APP_ENV=production`
	- `APP_HOST=0.0.0.0`
	- `APP_PORT=8000` (optional fallback only; runtime port is provided by Railway `PORT`)
	- `ALLOWED_ORIGINS=https://<your-vercel-domain>`
	- `ROBOFLOW_API_KEY=<your-key>`
	- `ROBOFLOW_API_URL=https://serverless.roboflow.com`
	- `ROBOFLOW_PROJECT_ID=<your-project-id>`
	- `ROBOFLOW_MODEL_VERSION=1`
5. Deploy and copy the Railway public URL, for example:
	- `https://your-backend.up.railway.app`

### Frontend (Vercel)

1. Import the same repository in Vercel.
2. Set the project root directory to `frontend`.
3. Add this environment variable in Vercel:
	- `NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app`
4. Deploy the frontend.

### Post deploy check

1. Open frontend URL from Vercel.
2. Trigger one analysis request.
3. Confirm backend responds on:
	- `https://your-backend.up.railway.app/api/v1`
