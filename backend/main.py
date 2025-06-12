# Build a FastAPI app with an endpoint to upload a .bin file and return summary using parser.py
import os
from dotenv import load_dotenv
load_dotenv()  # Add this near the top of your file
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import tempfile
import shutil
import uuid
from parser import parse_bin_file, summarize_telemetry
import groq

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in prod to allow only trusted frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Store parsed data in memory (for now)
session_data = {}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.bin'):
        raise HTTPException(status_code=400, detail="Only .bin files are allowed")

    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "log.bin")

    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        messages = parse_bin_file(temp_path)

        if isinstance(messages, dict) and "error" in messages:
            return {"filename": file.filename, "summary": messages}

        session_id = str(uuid.uuid4())
        session_data[session_id] = messages

        summary = summarize_telemetry(messages)
        summary["session_id"] = session_id

        return {"filename": file.filename, "summary": summary}
    except Exception as e:
        return {"filename": file.filename, "summary": {"error": f"Error processing file: {str(e)}"}}
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

class ChatRequest(BaseModel):
    session_id: str = Field(..., alias="sessionId")
    user_query: str = Field(..., alias="userQuery")

    class Config:
        allow_population_by_field_name = True


@app.post("/chat")
async def chat_with_agent(req: ChatRequest):
    session_id = req.session_id
    user_query = req.user_query
    print(" session id = ", session_id, " user query = ", user_query)

    if session_id not in session_data:
        return {"error": "No data found for this session"}

    messages = session_data[session_id]

    summary = summarize_telemetry(messages)


    message_types = list(summary.get("message_types", {}).keys())
    total_messages = summary.get("total_messages", 0)
    avg_altitude = summary.get("average_altitude", "Not available")

    prompt = f"""
You are an expert UAV log analyst. Your job is to analyze UAV telemetry logs and answer user questions.

Here is the summary of telemetry data:
- Total messages: {total_messages}
- Message types: {', '.join(message_types)}
- Average altitude: {avg_altitude}

Some sample messages:
{messages[:3]}

Look for:
- Sudden drops in altitude
- RC signal loss or failsafe events
- GPS glitches or low satellite counts
- Low battery voltage warnings
- Unusual mode transitions
- Errors or warnings in logs

User question: "{user_query}"

Please provide an accurate, technically insightful answer.
"""
    try:

        client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert UAV log analyst."},
                {"role": "user", "content": prompt}
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )

        if chat_completion.choices and chat_completion.choices[0].message:
            llm_response = chat_completion.choices[0].message.content
        else:
            llm_response = "No meaningful response from model."
        
    except Exception as e:
        return {"response": f"No response from model: {str(e)}", "session_id": session_id}

    return {
        "response": llm_response,
        "session_id": session_id
    }
