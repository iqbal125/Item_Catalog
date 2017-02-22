from time import strftime
import os
import jinja2
import random
from flask import Flask, render_template
from sqlalchemy.orm import sessionmaker
from database_setup import CPU, GPU
from sqlalchemy import create_engine
from database_setup import *

engine = create_engine('sqlite:///catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
def MainPage():
    return render_template("frontpage.html")

@app.route('/cpu')
def CPUPage():
    cpus = session.query(CPU).all()
    return render_template('cpupage.html', cpus=cpus)



if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
