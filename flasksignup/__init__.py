from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import os
import csv

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/signup', methods = ('GET','POST'))
    def signup():
        return render_template('signup.html')


    @app.route('/submit', methods = ['POST'])
    def submit():
        fname = request.form['firstname']
        lname = request.form['lastname']
        email = request.form['email']

        with open('flasksignup/static/info.csv','a') as file:
            writer = csv.writer(file)
            print(fname,lname,email)
            writer.writerow((fname,lname,email))

        return render_template('signup.html')


    return app