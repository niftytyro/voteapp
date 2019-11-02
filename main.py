from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys, os
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User> %r' %email

class Fighter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)


class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('votes', lazy='dynamic'))
    fighter_id = db.Column(db.Integer, db.ForeignKey('fighter.id'))
    fighter = db.relationship('Fighter', backref=db.backref('fighter', lazy='dynamic'))

@app.route('/', methods=['GET', 'POST'])
def home():
    email = None
    fighter_name = None
    message_level = None
    message = None
    if(request.method=='POST'):
        email = request.form.get('email')
        fighter = request.form.get('fighters')
        if(email and fighter):
            user = db.session.query(User).filter_by(email=email).first()
            if(user):
                message_level = "info"
                message = "You have already voted!"
            else:
                user = User(email=email)
                user = db.session.add(user)
                fighter = db.session.query(Fighter).filter_by(name=fighter).first()
                fighter_name = fighter.name
                vote = Votes(user=user, fighter=fighter)
                db.session.add(vote)
                db.session.commit()
                message_level = "success"
                message = "Your vote for %s has been succesfully submitted!" % fighter.name
        else:
            message_level = "error"
            message = "You must enter your email and select a wrestler to submit your vote."
    total_votes = db.session.query(Votes).count()
    vote_query = db.session.query(Votes.fighter_id, func.count(Votes.fighter_id))
    vote_counts = vote_query.group_by(Votes.fighter_id).order_by('fighter_id').all()
    return render_template("main.html", message_level=message_level, message=message, fighter=fighter_name, total_votes=total_votes, vote_counts=vote_counts)


if(__name__ == "__main__"):
    app.run()