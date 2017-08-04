import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='ABC123',
    USERNAME='eliel'
))
app.config.from_envvar('CHORES_SETTINGS', silent=True)

@app.route('/')
def show_chores():
    return render_template('show_chores.html')