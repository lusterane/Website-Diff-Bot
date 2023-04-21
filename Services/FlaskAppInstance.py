import os

from flask import Flask

app = Flask(__name__)

# configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SUPABASE_CONNECTION_STRING")
