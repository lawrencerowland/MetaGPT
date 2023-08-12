from surprise import Dataset, Reader, KNNBasic
from models import User, Contractor, Review
from sqlalchemy.orm import Session

class Recommender:
    def __init__(self, session: Session):
        self.session = session

    def train(self):
        # Fetch all reviews from the database
        reviews = self.session.query(Review).all()

        # Prepare the data for the recommendation algorithm
        data = [(review.user_id, review.contractor_id, review.rating) for review in reviews]
        reader = Reader(rating_scale=(1, 5))
        dataset = Dataset.load_from_df(data, reader)

        # Train the recommendation algorithm
        self.algorithm = KNNBasic()
        self.algorithm.fit(dataset.build_full_trainset())

    def recommend(self, user: User, n: int = 5):
        # Fetch all contractors from the database
        contractors = self.session.query(Contractor).all()

        # Prepare the data for the recommendation algorithm
        data = [(user.id, contractor.id, 0) for contractor in contractors]

        # Get the top n recommendations for the user
        predictions = [self.algorithm.predict(*d) for d in data]
        top_n = sorted(predictions, key=lambda p: p.est, reverse=True)[:n]

        # Return the recommended contractors
        return [self.session.query(Contractor).get(p.iid) for p in top_n]
