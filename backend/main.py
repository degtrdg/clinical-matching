import logging
import os
import time
import uuid

import dotenv
import openai
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

dotenv.load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RandRequest(BaseModel):
    query: str

class PatientInfo(BaseModel):
    # Define the patient information fields you expect
    # For example, name, age, medical_conditions, etc.
    name: str
    age: int
    medical_conditions: list

class ClinicalTrialResult(BaseModel):
    # Define the structure of the clinical trial results
    trial_id: str
    reasons: list

@app.post("/submit_patient_info")
async def submit_patient_info(request: PatientInfo):
    """
    Receives patient information and returns relevant clinical trials.
    @params:
        request: PatientInfo
    @returns:
        List of clinical trials and reasons
    """
    try:
        # Validate patient information
        validate_patient_info(request)
        
        # Query the database
        query_results = query_database(request)
        
        # Analyze with AI model
        analysis_results = analyze_with_ai_model(query_results)
        
        # Determine relevant clinical trials
        clinical_trials = determine_relevant_trials(analysis_results)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": clinical_trials,
            },
        )
    except Exception as e:
        return error_handler(request, e)

def validate_patient_info(request: PatientInfo):
    # Add logic to validate the patient information
    # For example, check if age is within a valid range
    pass

def query_database(request: PatientInfo):
    # Add logic to query the database with the patient information
    # This would involve interacting with your actual database
    pass

def analyze_with_ai_model(query_results):
    # Add logic to send the query results to the AI model
    # This would involve sending data to your AI model and receiving the analysis
    pass

def determine_relevant_trials(analysis_results):
    # Add logic to determine the relevant clinical trials
    # This would use the analysis results to filter and select trials
    pass

@app.post("/")
@app.get("/")
def root():
    return "hi"

@app.post("/rand_request")
async def rand_request_endpoint(
    request: RandRequest,
):
    """
    Saves a resource to a starterpac and returns a new ID and URL for the resource
    @params:
        query: str
    @returns:
        result: str
    """
    try:
        query = request.query

        if not query:
            raise ValueError("query is required")

        response = JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "result": "hi guys!",
                },
            },
        )
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as e:
        return error_handler(request, e)

def error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "data": {
                "error_message": str(exc),
            },
        },
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)