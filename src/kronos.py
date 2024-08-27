import os, requests
from dataclasses import dataclass
from datetime import datetime, timedelta, time
from .repository import create
from .schemas.availability import AvailabilityModel
from .schemas.shift import ShiftModel
from .schemas.possible_shift import PossibleShiftModel
from .models.availability import Availability
from .models.shift import Shift
from .models.possible_shift import PossibleShift
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class KronosAvailability():
    url = str(os.getenv('DOMAIN_URL'))
    company_slug = str(os.getenv('COMPANY_SLUG'))
    token_company = str(os.getenv('TOKEN_COMPANY'))
    
    async def get_availability(self, employees: dict, start_date: str, end_date: str, db: AsyncSession):
        person_nums = [e for e, id in employees.items()]
        result = requests.post( 
            url = f'{self.url}/api/v1/kronos_wfc/scheduler/availabilities',
            json = {
                'person_numbers': person_nums,
                'start_date': start_date,
                'end_date': end_date
            },
            headers = {
                'Authorization': f'Bearer {self.token_company}',
                'company': self.company_slug,
                'Content-Type': 'application/json'
            }
        )
        
        full_availabilities = []
        periods = await self.casting(result.json()['data'])
        availabilities = await self.transformation(employees, periods)
        if availabilities:
            full_availabilities.append(availabilities)

        if full_availabilities:
            full_availabilities = [AvailabilityModel(**item) for sublist in full_availabilities for item in sublist]
            await create(db, Availability, full_availabilities)
            return full_availabilities
        
        return "No data to insert"
    
    async def generate_data(self, steps_time):
            list_data = [0] * 96
            for step in steps_time:
                if step['type'] == 'Disponible':
                    start_time = step['start_time']
                    end_time = step['end_time']

                    start_time = int(start_time.split(':')[0]) * 4 + int(start_time.split(':')[1]) // 15
                    end_time = int(end_time.split(':')[0]) * 4 + int(round(float(end_time.split(':')[1])/15))

                    for i in range(start_time, end_time):
                        list_data[i] = 1

            string_data = ''.join([str(i) for i in list_data])
            return string_data

    async def casting(self, raw_data: dict):
        employees = {}
        if raw_data:
            for person_num, dates in raw_data.items():
                employees[person_num] = []
                for p, data in dates.items():
                    for d in data:
                        dates = []
                        start_time = datetime.strptime(d['start'], '%H:%M')
                        end_time = start_time + timedelta(hours=int(d['duration'].split(':')[0]), minutes=int(d['duration'].split(':')[1]))
                        if end_time.hour == 0 and end_time.minute == 0:
                            end_time = datetime.strptime('23:59', '%H:%M')

                        dates.append(
                            {
                                'type': d['type'],
                                'start_time': d['start'],
                                'end_time': datetime.strftime(end_time, '%H:%M')
                            }
                        )
                        employees[person_num].append({p: dates})

            return employees
    
    async def transformation(self, employee_data: dict, data: dict):
        if data: 
            availabilities = []
            for pn, dates in data.items():
                for p in dates:
                    for k, v in p.items():
                        data = await self.generate_data(v)
                        availabilities.append(
                            {
                                'employee_id': employee_data[pn],
                                'date': datetime.strptime(k, '%Y-%m-%d'),
                                'data': data
                            }
                        )

            return availabilities
        return False

class KronosShifts():
    url = str(os.getenv('DOMAIN_URL'))
    company_slug = str(os.getenv('COMPANY_SLUG'))
    token_company = str(os.getenv('TOKEN_COMPANY'))

    async def get_shifts(self, employees: dict, start_date: str, end_date: str, db: AsyncSession):
        full_shifts = []
        for employee, employee_id in employees.items():
            result = requests.get( 
                url = f'{self.url}/api/v1/kronos_wfc/schedule',
                params = {
                    'person_number': employee,
                    'start_date': start_date,
                    'end_date': end_date
                },
                headers = {
                    'Authorization': f'Bearer {self.token_company}',
                    'company': self.company_slug,
                    'Content-Type': 'application/json'
                }
            )
            
            shifts = await self.casting(result.json()['data'], employee_id)
            if shifts:
                full_shifts.append(shifts)
        
        if full_shifts:
            full_shifts = [ShiftModel(**item) for sublist in full_shifts for item in sublist]
            await create(db, Shift, full_shifts)
            return full_shifts

        return "No data to insert"
    
    async def casting(self, raw_data: dict, employee_id: int):
        listt = []
        if raw_data: 
            for k, s in raw_data.items():
                for shift in s:
                   start_ts = datetime.strptime(shift[0]['start'], '%Y-%m-%dT%H:%M:%S').time()
                   end_ts = datetime.strptime(shift[0]['end'], '%Y-%m-%dT%H:%M:%S').time()
                   duration = time(hour = shift[0]['amount'])
                   listt.append(
                       {
                            'employee_id': employee_id,
                            'date': shift[0]['date'],
                            'start_ts': start_ts,
                            'end_ts': end_ts,
                            'duration': duration,
                            'timezone': 'America/Santiago',
                            'override': shift[0]['locked'],
                            'scheduler_create': False,
                            'enable': True
                       }
                    )
                   
            return listt
        
        return False

