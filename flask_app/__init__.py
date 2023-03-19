from flask import Flask, render_template, request, redirect, session, flash
from datetime import datetime
app = Flask(__name__)
app.secret_key = "CHANGEME"
DB = "user"