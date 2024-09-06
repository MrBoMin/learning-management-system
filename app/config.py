import os

class Config:
    SECRET_KEY = 'secrete_key_222'
    SQLALCHEMY_DATABASE_URI ='sqlite:///lms.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
