from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Person(Base):
    __tablename__ = "osoby"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    
    town_id = Column(Integer, ForeignKey("miejscowosci.id"))
    company_branch_id = Column(Integer, ForeignKey("oddzialy_firmy.id"))

    town = relationship("Town", back_populates="people")
    company_branch = relationship("CompanyBranch", back_populates="employees")

class Town(Base):
    __tablename__ = "miejscowosci"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    people = relationship("Person", back_populates="town")

class Company(Base):
    __tablename__ = "firmy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    branches = relationship("CompanyBranch", back_populates="company", cascade="all, delete-orphan")

class CompanyBranch(Base):
    __tablename__ = "oddzialy_firmy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    company_id = Column(Integer, ForeignKey("firmy.id"))

    company = relationship("Company", back_populates="branches")
    employees = relationship("Person", back_populates="company_branch")