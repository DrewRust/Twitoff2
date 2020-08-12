#### ---> runs the app in the terminal:
#### FLASK_APP=twitoff_sub_dir:APP flask run
#### running flask shell will give you an interactive python environment
#### ---> how to interact with your database
####  FLASK_APP=twitoff_sub_dir:APP flask shell
#### creates an interactive shell
#### ---> then type: dir()
#### ---> then type: from twitoff_sub_dir.db_model import db, User, Tweet
#### now you have access to User and Tweet
#### ---> then type: db.init_app(app)
#### (above will associate db model with flask app)
#### ---> exit() gets you out of the shell env
#### db.create_all() will create the twitoff.sqlite

from flask import Flask, render_template, request
#### import User class
from .db_model import db, User
from .twitter import add_user_tweepy
from .predict import predict_user
#### where the initial app code will live


#### define function called create app
def create_app():
    '''Create and configure an instance of the Flask application'''

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/andrewrust/Twitoff/twitoff_sub_dir/twitoff.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.route('/')
    def root():
        #### render a template
        return render_template('base.html', title='Home', users=User.query.all())
        # return "Welcome to Twitoff!"

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_user_tweepy(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.username == name).one().tweet
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = 'Cannot compare a user to themselves'
        else:
            prediction = predict_user(user1, user2, tweet_text)

            message = '"{}" is more likely to be said by {} than {}'.format(
                tweet_text, user1 if prediction else user2, user2 if prediction else user1
            )

        return render_template('prediction.html', title='Prediction', message=message)

    return app