from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import Employee
from database import SessionLocal, engine
import database_models

from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database_models.Base.metadata.create_all(bind=engine)


class LoginData(BaseModel):
    email: str
    password: str


class ChangePassword(BaseModel):
    id: int
    old_password: str
    new_password: str


class ChangeEmail(BaseModel):
    id: int
    password: str
    new_email: str


employees = [
    Employee(
        id=1,
        name="Akash",
        email="akash@gmail.com",
        department="IT",
        salary=50000,
        role="Admin",
        password="Admin@123"
    ),
    Employee(
        id=2,
        name="Dinesh",
        email="dinesh@gmail.com",
        department="HR",
        salary=55000,
        role="HR",
        password="Hr@123"
    ),
    Employee(
        id=3,
        name="AAkash",
        email="aakash@gmail.com",
        department="IT",
        salary=60000,
        role="Employee",
        password="Emp@123"
    ),
    Employee(
        id=4,
        name="Anil",
        email="anil@gmail.com",
        department="IT",
        salary=50000,
        role="Manager",
        password="Manager@123"
    ),
    Employee(
        id=5,
        name="Kavi",
        email="kavi@gmail.com",
        department="HR",
        salary=60000,
        role="Employee",
        password="Emp@123"
    )
]

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()

    count = db.query(database_models.Employee).count()

    if count == 0:
        for employee in employees:
            db.add(database_models.Employee(**employee.model_dump()))

        db.commit()

    db.close()


init_db()


@app.get("/")
def home():
    return {"message": "Employee Management System"}


@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    employee = db.query(database_models.Employee).filter(
        database_models.Employee.email == data.email,
        database_models.Employee.password == data.password
    ).first()

    if employee:

        token = create_access_token({
           "sub": employee.email,
           "role": employee.role,
           "id": employee.id
    })

        return {
            "status": "success",
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "role": employee.role
    }

    return {
    "status": "failed",
    "message": "Invalid email or password"
}


@app.put("/change-password")
def change_password(data: ChangePassword, db: Session = Depends(get_db)):
    employee = db.query(database_models.Employee).filter(
        database_models.Employee.id == data.id,
        database_models.Employee.password == data.old_password
    ).first()

    if not employee:
        return {
            "status": "failed",
            "message": "Old password is wrong"
        }

    employee.password = data.new_password
    db.commit()

    return {
        "status": "success",
        "message": "Password changed successfully"
    }


@app.put("/change-email")
def change_email(data: ChangeEmail, db: Session = Depends(get_db)):
    employee = db.query(database_models.Employee).filter(
        database_models.Employee.id == data.id,
        database_models.Employee.password == data.password
    ).first()

    if not employee:
        return {
            "status": "failed",
            "message": "Password is wrong"
        }

    employee.email = data.new_email
    db.commit()

    return {
        "status": "success",
        "message": "Email changed successfully"
    }


# Admin: View all employees
@app.get("/admin/employees")
def admin_view_all(db: Session = Depends(get_db)):
    return db.query(database_models.Employee).all()


# Admin: Add employee
@app.post("/admin/employee")
def admin_add(employee: Employee, db: Session = Depends(get_db)):
    new_emp = database_models.Employee(**employee.model_dump())

    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return {"message": "Employee added successfully"}


# Admin: Update employee
@app.put("/admin/employee/{id}")
def admin_update(id: int, employee: Employee, db: Session = Depends(get_db)):
    db_emp = db.query(database_models.Employee).filter(
        database_models.Employee.id == id
    ).first()

    if db_emp:
        db_emp.name = employee.name
        db_emp.email = employee.email
        db_emp.department = employee.department
        db_emp.salary = employee.salary
        db_emp.role = employee.role
        db_emp.password = employee.password

        db.commit()

        return {"message": "Employee updated successfully"}

    return {"message": "Employee not found"}


# Admin: Delete employee
@app.delete("/admin/employee/{id}")
def admin_delete(id: int, db: Session = Depends(get_db)):
    db_emp = db.query(database_models.Employee).filter(
        database_models.Employee.id == id
    ).first()

    if db_emp:
        db.delete(db_emp)
        db.commit()

        return {"message": "Employee deleted successfully"}

    return {"message": "Employee not found"}


# HR: View all employees
@app.get("/hr/employees")
def hr_view_all(db: Session = Depends(get_db)):
    return db.query(database_models.Employee).all()


# HR: Add employee
@app.post("/hr/employee")
def hr_add(employee: Employee, db: Session = Depends(get_db)):
    new_emp = database_models.Employee(**employee.model_dump())

    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return {"message": "Employee added successfully"}


# HR: Update employee
@app.put("/hr/employee/{id}")
def hr_update(id: int, employee: Employee, db: Session = Depends(get_db)):
    db_emp = db.query(database_models.Employee).filter(
        database_models.Employee.id == id
    ).first()

    if db_emp:
        db_emp.name = employee.name
        db_emp.email = employee.email
        db_emp.department = employee.department
        db_emp.salary = employee.salary
        db_emp.role = employee.role
        db_emp.password = employee.password

        db.commit()

        return {"message": "Employee updated successfully"}

    return {"message": "Employee not found"}


# Employee: View own details
@app.get("/employee/{id}")
def employee_view_own(id: int, db: Session = Depends(get_db)):
    employee = db.query(database_models.Employee).filter(
        database_models.Employee.id == id
    ).first()

    if employee:
        return employee

    return {"message": "Employee not found"}


# Manager: View team details by department
@app.get("/manager/team/{department}")
def manager_view_team(department: str, db: Session = Depends(get_db)):
    return db.query(database_models.Employee).filter(
        database_models.Employee.department == department
    ).all()