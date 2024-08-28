import os, requests
from dataclasses import dataclass
from datetime import datetime, timedelta, time
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import create, flush
from .schemas.ruleset import RuleSetModel
from .schemas.availability import AvailabilityModel
from .schemas.shift import ShiftModel
from .schemas.possible_shift import PossibleShiftModel
from .schemas.shift_type import ShiftTypeModel
from .schemas.possible_shift_r_shift_type import PossibleShiftRShiftTypeModel
from .schemas.ruleset_assignment import RulesetAssignmentModel
from .models.ruleset import Ruleset
from .models.availability import Availability
from .models.shift import Shift
from .models.shift_type import ShiftType
from .models.possible_shift import PossibleShift
from .models.possible_shift_r_shift_type import PossibleShiftRShiftType
from .models.ruleset_assignment import RulesetAssignment


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

class KronosRuleSets():
    url = str(os.getenv('DOMAIN_URL'))
    company_slug = str(os.getenv('COMPANY_SLUG'))
    token_company = str(os.getenv('TOKEN_COMPANY'))

    async def get_rulesets(self, db: AsyncSession):
        result = requests.get(
            url = f'{self.url}/api/v1/kronos_wfc/scheduler/schedule_rules',
            headers = {
                'Authorization': f'Bearer {self.token_company}',
                'company': self.company_slug,
                'Content-Type': 'application/json'
            }
        )

        rulesets = await self.casting(result.json()['data'], db)

        return rulesets

    def hour_to_float(self, hour: str):
        return float(hour.split(':')[0]) + float(hour.split(':')[1]) / 60
    
    async def casting(self, raw_data: dict, db: AsyncSession):

        if raw_data:
            rulesets = []
            for name, rule in raw_data.items():
                if 'shift_profile_set' in rule:
                    rul = {
                        'name': name,
                        'description': rule['shift_profile_set']['description'],
                        'min_daily_hours': self.hour_to_float(rule['properties']['ERULE_MIN_HRS_DAY']['parameters']['ERPARAM_NZSCHED_HRS']['value']),
                        'max_daily_hours': self.hour_to_float(rule['properties']['ERULE_MAX_HRS_DAY']['parameters']['ERPARAM_SCHED_HRS']['value']),
                        'min_weekly_hours': self.hour_to_float(rule['properties']['ERULE_MIN_HRS_WK']['parameters']['ERPARAM_SCHED_HRS']['value']),
                        'max_weekly_hours': self.hour_to_float(rule['properties']['ERULE_MAX_HRS_WK']['parameters']['ERPARAM_SCHED_HRS']['value']),
                        'min_hours_between_shifts': self.hour_to_float(rule['properties']['ERULE_MIN_BTWN_SHFT']['parameters']['ERPARAM_INTER_SHIFT_SPAN']['value']),
                        'max_shift_segments_per_shift':int(rule['properties']['ERULE_MAX_SHIFTS_DAY']['parameters']['ERPARAM_SHIFTS']['value']),
                        'night_shift_start_time': time(hour=int(rule['night_start'].split(':')[0]), minute = int(rule['night_start'].split(':')[1])),
                        'night_shift_end_time': time(hour=int(rule['night_end'].split(':')[0]), minute = int(rule['night_end'].split(':')[1])),
                        'min_days_worked_per_week': int(rule['properties']['ERULE_MIN_DAYS_WK']['parameters']['ERPARAM_SCHED_DAYS']['value']),
                        'max_days_worked_per_week': int(rule['properties']['ERULE_MAX_DAYS_WK']['parameters']['ERPARAM_SCHED_DAYS']['value']),
                        'max_consecutive_work_days': int(rule['properties']['ERULE_MAX_CONSEC_DAYS']['parameters']['ERPARAM_CONSEC_DAYS']['value']),
                        'max_night_shifts_per_week': int(rule['properties']['ERULE_MAX_NIGHTS_WK']['parameters']['ERPARAM_NIGHTS']['value'] if 'ERULE_MAX_NIGHTS_WK' in rule['properties'] else 0),
                        'is_active': True if rule['is_active'] == 'true' else False,
                    }
                
                    # ask for the shift profile

                    shift_profile = {'name': rule['shift_profile_set']['name'], 'description': rule['shift_profile_set']['description']}
                    
                    possible_shift = PossibleShiftModel(**shift_profile)
                    possible_shift = await create(db, PossibleShift, [possible_shift])

                    rul['possible_shift_id'] = int(possible_shift[0].possible_shift_id)

                    # ask for the shifts types

                    instances: dict = rule['shift_profile_set']['instances']
                    pssbl_shft_r_shft_typ = []
                    for day, data in instances.items():
                        day = day.lower()
                        start, end, duration = [], [], []
                        for shifts in data:
                            start.append(time(hour=int(shifts['properties']['max_start_time'].split(':')[0]), minute = int(shifts['properties']['max_start_time'].split(':')[1])))
                            end.append(time(hour=int(shifts['properties']['max_end_time'].split(':')[0]), minute = int(shifts['properties']['max_end_time'].split(':')[1])))
                            duration.append(time(hour=int(shifts['properties']['max_duration'].split(':')[0]), minute = int(shifts['properties']['max_duration'].split(':')[1])))
                    
                        shift_type_ids = select(ShiftType.shift_type_id).where(
                            and_(
                                ShiftType.start_time.in_(start),
                                ShiftType.end_time.in_(end),
                                ShiftType.duration.in_(duration)
                            )
                        )

                        shift_type_ids = await db.execute(shift_type_ids)
                        shift_type_ids = shift_type_ids.scalars().all()

                        for shift_type_id in shift_type_ids:
                            value = {
                                'possible_shift_id': possible_shift[0].possible_shift_id,
                                'shift_type_id': shift_type_id,
                                f'{day}': True,
                            }
                            pssbl_shft_r_shft_typ.append(PossibleShiftRShiftTypeModel(**value))
                    
                    await create(db, PossibleShiftRShiftType, pssbl_shft_r_shft_typ)
                    rulesets.append(rul)
                    
            rulesets = [RuleSetModel(**item) for item in rulesets]
            rulesets = await create(db, Ruleset, rulesets)

            # ask for assignament of the rulesets to the employees

            assingments = requests.post(
                url = f'{self.url}/api/v1/kronos_wfc/scheduler/schedule_rules_assignments',
                json = {
                    'start_date': datetime.now().strftime('%Y-%m-%d'),
                    'end_date': datetime.now().strftime('%Y-%m-%d'),
                    'person_numbers': ['*']
                },
                headers = {
                    'Authorization': f'Bearer {self.token_company}',
                    'company': self.company_slug,
                    'Content-Type': 'application/json'
                }
            )

            document_employees = []
            ruleset_names = []

            for docum, data in assingments.json()['data'].items():
                document_employees.append(docum)
                for rule in data:
                    ruleset_names.append(rule['rule_name'])
            
            ruleset_ids = select(Ruleset.ruleset_id).where(Ruleset.name.in_(ruleset_names))
            ruleset_ids = await db.execute(ruleset_ids)
            ruleset_ids = ruleset_ids.scalars().all()

            rulesetss = {}

            for rule_name, ruleset_id in zip(ruleset_names, ruleset_ids):
                rulesetss[rule_name] = ruleset_id

            employees_integrations = os.getenv('EMPLOYEE_URL')

            employees_ids = requests.post(
                url = f'{employees_integrations}/get_employees_ids/by_document_employee',
                json = document_employees
            )

            document_employee_r_employee_id = employees_ids.json()

            rulesets_assignaments = []

            for document_employee, data in assingments.json()['data'].items():
                if document_employee in document_employee_r_employee_id:
                    for rule in data:
                        if rule['rule_name'] in rulesets:
                            assingament = {
                                'employee_id': document_employee_r_employee_id[document_employee],
                                'ruleset_id': rulesetss[rule['rule_name']],
                                'start_date': datetime.strptime(rule['effective_date'], '%Y-%m-%d'),
                                'end_date': datetime.strptime(rule['expiration_date'], '%Y-%m-%d'),
                                'last_modified': datetime.now().strftime('%Y-%m-%d'),
                            }

                            rulesets_assignaments.append(assingament)
            
            rulesets_assignaments = [RulesetAssignmentModel(**item) for item in rulesets_assignaments]
            await create(db, RulesetAssignment, rulesets_assignaments)

            return rulesets
                    

