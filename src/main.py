from fastapi import FastAPI, Depends
from .kronos import KronosAvailability, KronosShifts, KronosRuleSets, KronosForecast
from .schemas.schemas import BaseRequest, ForecastRequest
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

@app.post('/loading_rulesets', tags=["Rulesets"])
async def loading_rulesets(db: AsyncSession = Depends(get_db)):
    kronos = KronosRuleSets()
    rulesets = await kronos.get_rulesets(db)
    return rulesets

@app.post('/loading_forecast', tags=["Forecast"])
async def loading_forecast(data: ForecastRequest, db: AsyncSession = Depends(get_db)):
    kronos = KronosForecast()
    rulesets = await kronos.get_forecast(data.path,data.start_date, data.end_date, db)
    return rulesets


    


