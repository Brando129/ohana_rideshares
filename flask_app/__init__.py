from flask import Flask

app = Flask(__name__)

app.secret_key = "Keep it secret, keep it safe"