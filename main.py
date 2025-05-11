import json
from typing import List

import pydantic
import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from database import get_session
from models import Department, Employee

app = FastAPI()

templates = Jinja2Templates(directory="templates")

if hasattr(pydantic.main, 'BaseConfig'):
    pydantic.main.BaseConfig.arbitrary_types_allowed = True

@app.get("/employees/", response_class=HTMLResponse)
def employee_list(request: Request, session: Session = Depends(get_session)):
    # employees = session.exec(select(Employee))
    # results from query require flattening to dicts in order to jsonable_encode them.
    # stmt = select(Employee, Department).where(Employee.department_id == Department.id)
    # results = session.exec(stmt).all()
    stmt = select(Employee, Department).join(Department, Employee.department_id == Department.id)
    results = session.exec(stmt).all()

    employee_data = [
        {
        "employee": employee.dict(),
        "department": department.dict()
    }  for employee, department in results
    ]

    employee_data_json = jsonable_encoder(employee_data)
    departments = set([e['department']['name'] for e in employee_data_json])

    context = {
        'request': request,
        'employees': employee_data_json,
        'departments': departments,
    }
    return templates.TemplateResponse("employees.html", context)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)