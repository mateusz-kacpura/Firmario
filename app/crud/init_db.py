from sqlalchemy.orm import Session
from app.models.models import Company, CompanyBranch, Town, Person
import datetime

def initialise_db(db: Session):
    # Sprawdź, czy dane już istnieją
    if db.query(Company).first():
        return

    # Tworzenie Firm
    company1 = Company(name="TechCorp")
    company2 = Company(name="HealthData")
    db.add_all([company1, company2])
    db.commit()

    # Tworzenie Oddziałów
    branch1a = CompanyBranch(name="Warszawa", company_id=company1.id)
    branch1b = CompanyBranch(name="Kraków", company_id=company1.id)
    branch2a = CompanyBranch(name="Gdańsk", company_id=company2.id)
    db.add_all([branch1a, branch1b, branch2a])
    db.commit()
    
    # Tworzenie Miejscowości
    town1 = Town(name="Warszawa")
    town2 = Town(name="Kraków")
    town3 = Town(name="Gdańsk")
    db.add_all([town1, town2, town3])
    db.commit()

    # Tworzenie Osób
    person1 = Person(first_name="Jan", last_name="Kowalski", birth_date=datetime.date(1985, 5, 20), town_id=town1.id, company_branch_id=branch1a.id)
    person2 = Person(first_name="Anna", last_name="Nowak", birth_date=datetime.date(1992, 9, 10), town_id=town2.id, company_branch_id=branch1b.id)
    person3 = Person(first_name="Piotr", last_name="Wiśniewski", birth_date=datetime.date(1988, 11, 30), town_id=town3.id, company_branch_id=branch2a.id)
    person4 = Person(first_name="Katarzyna", last_name="Zielińska", birth_date=datetime.date(1995, 2, 1), town_id=town1.id, company_branch_id=branch1a.id)

    db.add_all([person1, person2, person3, person4])
    db.commit()