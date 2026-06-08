from pydantic import BaseModel

class Employee(BaseModel):
    id: int
    name: str
    email: str
    department: str
    salary: int
    role: str
    password: str