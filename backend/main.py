from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()


@app.get("/")
async def welcome():
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
    