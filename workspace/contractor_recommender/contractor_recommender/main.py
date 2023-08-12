from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from views import login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

login_manager.init_app(app)

if __name__ == '__main__':
    from models import User, Contractor, Review, UserContractor
    db.create_all()
    app.run(debug=True)
