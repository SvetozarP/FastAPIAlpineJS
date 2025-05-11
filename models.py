from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from models import Employee  # Prevent circular imports

class Department(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    employees: List["Employee"] = Relationship(back_populates="department")


class Employee(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str
    surname: str
    job_title: str
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    department: Optional["Department"] = Relationship(back_populates="employees")
