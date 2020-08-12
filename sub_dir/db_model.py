
'''SQLAlchemy models for Twitoff'''
from flask_sqlalchemy import SQLAlchemy

#### flask_sqlalchemy makes using sql easy in flask

#### instantiate SQLAlchemy table
db = SQLAlchemy()

#### creates User table with the db.Column method
class User(db.Model):
    #### primary key will auto update
    id = db.Column(db.BigInteger, primary_key=True)
    #### username does have to be unique
    username = db.Column(db.String(80), unique=True, nullable=False)
    follower_count = db.Column(db.Integer, nullable=False)
    # Tweet ID's are ordinal ints, so we can fetch most recent tweets
    newest_tweet_id = db.Column(db.BigInteger, nullable=False)
    #### dunder method will print the users name when referenced
    #### will return only username
    def __repr__(self):
        return '<User %r>' % self.username


class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    #### text is stored as db.Unicode so we can process text later
    text = db.Column(db.Unicode(300))
    #### below is a db.relationship e.g. one to many etc
    #### select 'User' table then backref 'tweet' also 'User' table will be 'user'
    #### PickleType could be any Python data structure
    embedding = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweet', lazy=True))

    def __repr__(self):
        return '<Tweet %r>' % self.text