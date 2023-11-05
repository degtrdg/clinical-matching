import uvicorn

# import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, HTTPException
import pandas as pd
from fastapi import File
import httpx
from module.agent import get_patient_match_result
from module.helpers import get_top_5_trials

# dotenv.load_dotenv(".env")
# openai.api_key = os.environ.get("OPENAI_API_KEY")

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

class PatientRequest(BaseModel):
    patient: str

@app.post("/")
@app.get("/")
def root():
    return "hi"


@app.post("/uploadcsv/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.filename.endswith(".csv"):
        dataframe = pd.read_csv(file.file)

        modelResponse = httpx.post("https://api.huggingface.com/", data=dataframe)
        return dataframe.to_dict("records")
    else:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a CSV file."
        )

@app.post("/get_patient_match_result/")
async def get_patient_match_result_endpoint(
    request: PatientRequest,
):
    """
    Saves a resource to a starterpac and returns a new ID and URL for the resource
    @params:
        query: str
    @returns:
        result: str
    """
    try:
        patient = request.patient

        # Get the top 5 clinical trials through embedding search
        top_5_trials = get_top_5_trials(patient_report=patient)

        if not patient:
            raise ValueError("query is required")
        
        results = []
        for document, metadata in zip(top_5_trials["documents"], top_5_trials["metadata"]):
            results.append( {
                    "patient_match_result": get_patient_match_result(patient_report=patient, clinical_trial=document),
                    "metadata": metadata
                })
        
        response = JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "result": results
                },
            },
        )
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as e:
        return error_handler(request, e)



# This is gonna get data from the  embeddings database
@app.post("/get_data/")
async def get_data(file: UploadFile = File(...)):
    data = pd.read_csv(file.file)
    return "This is a test"


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
    uvicorn.run(app, host="0.0.0.0", port=80)
