from typing import List 
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pydantic

from models import Employee, Department


app = FastAPI()

templates = Jinja2Templates(directory="templates")

if hasattr(pydantic.main, 'BaseConfig'):
    pydantic.main.BaseConfig.arbitrary_types_allowed = True

@app.get("/employees/", response_class=HTMLResponse)
def employee_list(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("employees.html", context)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)