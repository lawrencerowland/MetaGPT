## models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    saved_contractors = relationship('Contractor', secondary='user_contractor')

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Contractor(Base):
    __tablename__ = 'contractors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    reviews = relationship('Review', backref='contractor')

    def __init__(self, name: str, specialty: str, rating: float, description: str):
        self.name = name
        self.specialty = specialty
        self.rating = rating
        self.description = description


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    contractor_id = Column(Integer, ForeignKey('contractors.id'))

    def __init__(self, content: str, rating: float, user: User, contractor: Contractor):
        self.content = content
        self.rating = rating
        self.user = user
        self.contractor = contractor


class UserContractor(Base):
    __tablename__ = 'user_contractor'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    contractor_id = Column(Integer, ForeignKey('contractors.id'), primary_key=True)
