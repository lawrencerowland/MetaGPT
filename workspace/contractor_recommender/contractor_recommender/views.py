from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User, Contractor, Review
from forms import RegistrationForm, LoginForm, ContractorForm, ReviewForm
from recommender import Recommender
from sqlalchemy.orm import Session

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
recommender = Recommender(Session())

@app.route('/')
@login_required
def home():
    recommendations = recommender.recommend(current_user)
    return render_template('home.html', recommendations=recommendations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        Session.add(user)
        Session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Session.query(User).filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/contractor/<int:contractor_id>')
@login_required
def contractor(contractor_id):
    contractor = Session.query(Contractor).get(contractor_id)
    return render_template('contractor.html', contractor=contractor)

@app.route('/review/<int:contractor_id>', methods=['GET', 'POST'])
@login_required
def review(contractor_id):
    form = ReviewForm()

    if form.validate_on_submit():
        contractor = Session.query(Contractor).get(contractor_id)
        review = Review(form.content.data, form.rating.data, current_user, contractor)
        Session.add(review)
        Session.commit()
        flash('Review submitted successfully.', 'success')
        return redirect(url_for('contractor', contractor_id=contractor_id))

    return render_template('review.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return Session.query(User).get(int(user_id))
