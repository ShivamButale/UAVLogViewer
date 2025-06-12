# UAV Log Viewer

![log seeking](preview.gif "Logo Title Text 1")

 This is a Javascript based log viewer for Mavlink telemetry and dataflash logs.
 [Live demo here](http://plot.ardupilot.org).

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

# Docker

run the prebuilt docker image:

``` bash
docker run -p 8080:8080 -d ghcr.io/ardupilot/uavlogviewer:latest

```

or build the docker file locally:

``` bash

# Build Docker Image
docker build -t <your username>/uavlogviewer .

# Run Docker Image
docker run -e VUE_APP_CESIUM_TOKEN=<Your cesium ion token> -it -p 8080:8080 -v ${PWD}:/usr/src/app <your username>/uavlogviewer

# Navigate to localhost:8080 in your web browser

# changes should automatically be applied to the viewer

```

🧠 Chatbot Extension (Coding Challenge Submission)
This fork adds a FastAPI-based backend with LLM integration for telemetry-aware chatbot functionality.

## 🚀 Features

- Upload `.bin` UAV log files
- Ask natural language questions like:
  - "Did the UAV crash?"
  - "Was there a GPS glitch?"
  - "Any signal loss during flight?"
- Answers based on telemetry data (`RCIN`, `GPS`, `BAT`, etc.)
- Groq LLM integration via Python backend
- Automatic session ID detection
- `.env` support for secure API key management

🧪 How to Run
1. Clone the repo and install frontend

```bash
git clone https://github.com/<your-username>/UAVLogViewer.git
cd UAVLogViewer
npm install
npm run dev
```

2. Setup and run backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a .env file in backend/ with this content:
```bash
GROQ_API_KEY=your_actual_key_here
```

Then run the server:
```bash
uvicorn main:app --reload
```
Frontend: http://localhost:8080
Backend API: http://localhost:8000/docs

Watch demo video of the chatbot integration:
https://drive.google.com/file/d/11egjB3f9EXFflnEIcMfQV6jZwNFlBWIA/view?usp=sharing