from fastapi import FastAPI

app = FastAPI(title="Team geogusser adeptus API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}