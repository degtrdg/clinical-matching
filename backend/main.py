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