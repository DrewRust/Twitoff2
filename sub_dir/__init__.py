'''Entry point to the Twitoff Flask application'''

#### importing app.py the create_app funtion
from .app import create_app

#### create the app with a global variable APP which is why it's all caps
APP = create_app()