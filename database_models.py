from sqlalchemy import Column, Integer, String
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    department = Column(String(100))
    salary = Column(Integer)
    role = Column(String(20))
    password = Column(String(100))