import os
from flask import Flask
import secrets
app = Flask(__name__)
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ["SERPAPI_API_KEY"] = '228480454d680012919886e34fc1f099637dd5c26a9e8b7ca3422b8540dcc8d4'
app.secret_key = secrets.token_hex(16)
from .routes.index import index, train,chat 

