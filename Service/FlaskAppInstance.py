from flask import Flask, make_response
import os

app = Flask(__name__)

# configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SUPABASE_CONNECTION_STRING")
