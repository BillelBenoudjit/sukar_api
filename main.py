from fastapi import FastAPI

from quantum import get_outcome

app = FastAPI()

# uvicorn main:app --reload

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/simulate")
async def simulate(input: str):
    result = get_outcome(input)
    return result