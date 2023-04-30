from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from quantum import get_outcome
from local_quantum import get_local_outcome

from typing import List

# uvicorn main:app --reload

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# uvicorn main:app --reload

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/simulate")
async def simulate(input):
    result: List[str] = []
    result = get_outcome(input)
    return result

@app.get("/local_simulate")
async def simulate():
    result: List[str] = []
    result = get_local_outcome()
    return result