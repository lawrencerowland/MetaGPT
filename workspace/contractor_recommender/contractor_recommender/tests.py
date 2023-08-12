import pytest
from models import User, Contractor, Review
from recommender import Recommender
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)

def test_user():
    session = Session()
    user = User('testuser', 'testuser@example.com', 'password')
    session.add(user)
    session.commit()
    assert session.query(User).filter_by(username='testuser').first() is not None

def test_contractor():
    session = Session()
    contractor = Contractor('testcontractor', 'plumbing', 4.5, 'Test description')
    session.add(contractor)
    session.commit()
    assert session.query(Contractor).filter_by(name='testcontractor').first() is not None

def test_review():
    session = Session()
    user = session.query(User).filter_by(username='testuser').first()
    contractor = session.query(Contractor).filter_by(name='testcontractor').first()
    review = Review('Test review', 4.5, user, contractor)
    session.add(review)
    session.commit()
    assert session.query(Review).filter_by(content='Test review').first() is not None

def test_recommender():
    session = Session()
    recommender = Recommender(session)
    recommender.train()
    user = session.query(User).filter_by(username='testuser').first()
    recommendations = recommender.recommend(user)
    assert len(recommendations) > 0
