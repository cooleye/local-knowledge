import os
from flask import Flask

app = Flask(__name__)
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

from localknowledge.routes.index import *
