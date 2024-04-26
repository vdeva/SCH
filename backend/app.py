from fastapi import FastAPI
from tree import process_debate

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/call_model/")
async def post_model_call(history: str):
    tweet_context = "The first opponent argument is a tweet that is attacking the reputation of the Silicon Valley Bank. Your answer needs to be very short and impactful as a Tweet. "
    return process_debate(tweet_context + history)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8400)
