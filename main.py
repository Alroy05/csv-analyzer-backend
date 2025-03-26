from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
import uuid
from pymongo import MongoClient
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["rag_csv"]
collection = db["csv_files"]

# Google Gemini AI Setup
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

UPLOAD_DIR = "uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    file_id: str
    query: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())  # Generate a unique ID for the file
        original_filename = file.filename  # Get the original filename
        file_extension = os.path.splitext(original_filename)[-1]  # Get the file extension
        safe_filename = f"{file_id}{file_extension}"  # Ensure uniqueness

        file_path = os.path.join(UPLOAD_DIR, safe_filename)  # Save as original name
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        df = pd.read_csv(file_path)
        records = df.to_dict(orient="records")

        # Store the original filename instead of "file"
        collection.insert_one({
            "file_id": file_id,
            "file_name": original_filename,
            "file_path": file_path,  # Store the actual path
            "document": records
        })

        return {"file_id": file_id, "file_name": original_filename, "message": "Upload successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage Error: {str(e)}")

@app.get("/files")
async def list_files():
    try:
        files = list(collection.find({}, {"_id": 0, "file_id": 1, "file_name": 1}))
        return {"files": files}
    except:
        raise HTTPException(status_code=500, detail="Failed to retrieve files")

@app.get("/preview/{file_id}")
async def preview_csv(file_id: str):
    file_data = collection.find_one({"file_id": file_id})
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    df = pd.DataFrame(file_data["document"])
    return df.head(5).to_dict(orient="records")  # Return first 5 rows

@app.post("/query")
async def query_file(query_request: QueryRequest):
    file_data = collection.find_one({"file_id": query_request.file_id})
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    csv_content = file_data["document"]
    csv_text = "\n".join([str(row) for row in csv_content])

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"CSV Data:\n{csv_text}\n\nQuery: {query_request.query}")

    return {"response": response.text}

@app.delete("/file/{file_id}")
async def delete_file(file_id: str):
    file_data = collection.find_one({"file_id": file_id})
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")

    collection.delete_one({"file_id": file_id})
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"message": "File deleted successfully"}
