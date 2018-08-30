from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def create_app(test_config=None):
    gmail_password = input('Input Gmail Password\n')
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


    @app.route('/', methods = ('GET','POST'))
    def home():
        return redirect('/signup')

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

            gmail_user = 'nano.pclub@gmail.com'

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user,gmail_password)

            #EMAIL HTML HEREEEEEE!!!!!!!!!!!!!!
            email_html = """
                         <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                         <html xmlns="http://www.w3.org/1999/xhtml">
                          <head>
                           <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                           <title>PClub Email</title>
                           <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                         </head>

                         <!-- Start Body -->
                         <body style="margin: 0; padding: 0;">
                           <table align="center" border="0" cellpadding="0" cellspacing="0" width="500px" style = "border-collapse: collapse;">
                             <tr>
                               <td align="center" bgcolor="#ffffff" style="padding: 30px 0 20px 0;">
                                 <img src="cid:med_logo.png" alt="PCLUB_LOGO.png" width="100%" height="auto" style=" margin-bottom: 20px; display: block;">
                                 <hr>
                               </td>
                             </tr>

                             <tr>
                               <td style="border-spacing: 20px; padding-left: 10px; " >
                                 <h3 style="font-family: Helvetica; color: rgb(0, 44, 115);"><span style="color: rgb(255, 192, 46);">//</span> Welcome!</h3>
                               </td>
                             </tr>
                             <tr bgcolor  = "#ffffff">
                               <td align = "left" style="padding: 20px 10px 20px 10px;">
                                 &nbsp;&nbsp;&nbsp;&nbsp;Thank you for your interest in Programming Club! Our goal is to organize interesting software development projects and allow CNSE students to develop their interest and skills in Computer Science.
                                 This semester, we will be working on building an Arduino-powered LED cube based on the prototype we demoed at the club fair.
                                 <br> <br>
                                 &nbsp;&nbsp;&nbsp;&nbsp;If you are new to programming, we will be hosting an introduction to Python course. For those with prior coding experience, we will also offer a class on Web development if there is enough interest.
                                 Courses are open to everyone and do not require signup. Feel free to only come to the classes if you are not interested in the projects, or vice versa.
                               </td>
                             </tr>
                             <tr>
                               <td style="border-spacing: 20px; padding-left: 10px; " >
                                 <h3 style="font-family: Helvetica; color: rgb(0, 44, 115);"><span style="color: rgb(255, 192, 46);">//</span> Interest and Availability Survey </h3>
                               </td>
                             </tr>
                             <tr>
                               <td style="padding: 20px 10px 20px 10px;">
                                 We plan on setting our weekly meetings at a time that works best for everyone. Please fill out the attached google form by <b>Tuesday, Sept 4th</b>. Our first meeting will likely be the week of September 10-14. Stay tuned for more information!
                               </td>
                             </tr>
                             <tr align = "center">
                               <td> <a href="https://docs.google.com/forms/d/e/1FAIpQLSdW7Aes6qiYkoHeE0iWGz2nBjPaHAu7x-7EJEjztBSteSa0lQ/viewform">Find the survey here</a> </td>
                             </tr>

                           </table>
                         </body>
                         </html>


                         """

            imgpath = "static/med_logo.png"
            imgdata = app.open_resource(imgpath, 'rb').read()


            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Welcome to Programming Club'
            msg['To'] = email
            msg['From'] = gmail_user


            img = MIMEImage(imgdata)
            img.add_header('Content-ID', '<{}>'.format("med_logo.png"))
            msg.attach(img)

            part1 = MIMEText(email_html, 'html')
            msg.attach(part1)

            server.send_message(msg)

        return redirect('/signup')


    return app
