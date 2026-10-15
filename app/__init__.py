from flask import Flask
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

from app import routes