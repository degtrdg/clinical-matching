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
from gradio_client import Client
from module.get_data import get_data, open_file

# dotenv.load_dotenv(".env")
# openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()
clusts = "C:\\Users\\joewc\\OneDrive\\Desktop\\HackUTD\\clinical-matching\\backend\\module\\clusts_dict.pickle"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cancer_types = [
    "Adrenocortical carcinoma (ACC)",
    "Bladder urothelial carcinoma (BLCA)",
    "Ovarian serous cystadenocarcinoma (OV)",
    "Cervical squamous cell carcinoma and endocervical adenocarcinoma (CESC)",
    "Cholangiocarcinoma (CHOL)",
    "Colon adenocarcinoma (COAD)",
    "Lymphoid neoplasm diffuse large B-cell lymphoma (DLBC)",
    "Esophageal carcinoma (ESCA)",
    "Glioblastoma multiforme (GBM)",
    "Head and Neck squamous cell carcinoma (HNSC)",
    "Kidney chromophobe (KICH)",
    "Kidney renal clear cell carcinoma (KIRC)",
    "Kidney renal papillary cell carcinoma (KIRP)",
    "Acute myeloid leukemia (LAML)",
    "Brain lower grade glioma (LGG)",
    "Liver hepatocellular carcinoma (LIHC)",
    "Lung adenocarcinoma (LUAD)",
    "Lung squamous cell carcinoma (LUSC)",
    "Mesothelioma (MESO)",
    "Breast invasive carcinoma (BRCA)",
    "Pancreatic adenocarcinoma (PAAD)",
    "Pheochromocytoma and paraganglioma (PCPG)",
    "Prostate adenocarcinoma (PRAD)",
    "Rectum adenocarcinoma (READ)",
    "Sarcoma (SARC)",
    "Skin cutaneous melanoma (SKCM)",
    "Breast invasive carcinoma (BRCA)",
    "Testicular germ cell tumors (TGCT)",
    "Thyroid carcinoma (THCA)",
    "Thymoma (THYM)",
    "Uterine corpus endometrial carcinoma (UCEC)",
    "Uterine carcinosarcoma (UCS)",
    "Uveal melanoma (UVM)",
    "Normal Tissue (NORM)",
]


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
    if file.filename.endswith(".csv") or file.filename.endswith(".txt"):
        dataframe = pd.read_csv(file.file, header=0, index_col=0, sep=",")
        dataframe = dataframe.iloc[:, 0]
        header = [dataframe.name]

        # Extract the data; this skips the first element
        data = [[item] for item in dataframe.iloc[1:]]
        # Combine into the desired format
        result = {"headers": header, "data": data}
        # Set the client and then pass the info
        client = Client("https://arnav-jain1-clinical-matching.hf.space/--replicas/9nhzd/")
        result = client.predict(result, api_name="/predict")

        # Convert result to dict with cancer_types as keys
        result_dict = dict(zip(cancer_types, result.get("output")))

        # Sort the dict by values in descending order
        sorted_result = dict(
            sorted(result_dict.items(), key=lambda item: item[1], reverse=True)
        )

        # Get the top 5 items
        top_5 = dict(list(sorted_result.items())[:5])
        return top_5
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
        for document, metadata in zip(
            top_5_trials["documents"], top_5_trials["metadata"]
        ):
            results.append(
                {
                    "patient_match_result": get_patient_match_result(
                        patient_report=patient, clinical_trial=document
                    ),
                    "metadata": metadata,
                }
            )

        response = JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {"result": results},
            },
        )
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as e:
        return error_handler(request, e)


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
