from fastapi import FastAPI
from tree import process_debate

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/call_model/")
async def post_model_call(history: str):
    return process_debate(history)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8400)
