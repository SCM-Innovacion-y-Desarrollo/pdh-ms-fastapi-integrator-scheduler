from fastapi import FastAPI

app = FastAPI(
    title="Scheduler integrator",
    description="This is the integrator service for scheduler db",
    version="0.0.1"
)

@app.get("/")
async def root():
    return {'status': 'ok'}


    


