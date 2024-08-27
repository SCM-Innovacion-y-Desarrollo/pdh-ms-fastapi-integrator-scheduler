from fastapi import FastAPI, Depends
from .kronos import KronosAvailability, KronosShifts
from .schemas.schemas import BaseRequest
from .databases import get_db
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI(
    title="Scheduler integrator",
    description="This is the integrator service for scheduler db",
    version="0.0.1"
)

@app.get("/")
async def root():
    return {'status': 'ok'}

@app.post('/loading_availabilities', tags=["Availabilities"])
async def loading_availabilities(data: BaseRequest, db: AsyncSession = Depends(get_db)):
    kronos = KronosAvailability()
    avail = await kronos.get_availability(data.person_nums, data.start_date, data.end_date, db)
    return avail

@app.post('/loading_shifts', tags=["Shifts"])
async def loading_shifts(data: BaseRequest, db: AsyncSession = Depends(get_db)):
    kronos = KronosShifts()
    shifts = await kronos.get_shifts(data.person_nums, data.start_date, data.end_date, db)
    return shifts


    


