from flask import Flask, render_template, url_for, request, redirect, session
from flask import make_response, send_from_directory
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import calendar
import datetime
import math

load_dotenv()
cred = credentials.Certificate(os.getenv("serviceAccountKey"))
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'





def getData(matric, temp, assignNo, assignSubmitted, resource, totalAssign,percentage):
    
    Users = firestore_db.collection(u'Users').document(matric).collection("Subjects").stream()

    for user in Users:
        temp.append(user.to_dict()) 

  
    i = -1
    j = -1
    duedate = []
    for subject in temp:
        # print(subject)
        i= i + 1
        assignNo.append(0)
        assignSubmitted.append(0)
        resource.append(0)
        totalAssign.append(0)
        for subTopic in subject['subTopic']:
        
            j = j+1
            if "assign" in str(subTopic):
                totalAssign[i] =  totalAssign[i] + 1 
            if "resource" in str(subTopic):
                resource[i] = resource[i] + 1 
            if "Submitted" in str(subTopic):
                assignSubmitted[i] = assignSubmitted[i] + 1
            elif "No attempt" in str(subTopic):
                if "Due date" in str(subTopic):
                    duedate.append(subTopic["Due date"])
            
                assignNo[i] = assignNo[i] + 1


    for duration in duedate:
            
        overallDone = 0
        overallNotDone = 0
        for assignSub in assignSubmitted:
            overallDone = assignSub + overallDone
        for assignNot in assignNo:
            overallNotDone = assignNot +overallNotDone

        labels = 'Submmited' , 'No attempt'
        plt.rcParams['font.size'] = 20.0
        explode = (0, 0.1)  


        sizes = [overallDone,overallNotDone]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90,pctdistance=1.2, labeldistance=0.5,colors = ['lightblue','orange'])
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        fig1.savefig('static/my_plot.png')
    
        for i in range(len(assignSubmitted)):
            percentage.append(round((assignSubmitted[i]/(assignSubmitted[i]+assignNo[i])) * 100))
        print(percentage)


@app.route('/')
@app.route('/html&css/pages/dashboard/sign-in.html' ,methods = ['POST'])
def home():
    return render_template('html&css/pages/dashboard/sign-in.html')


@app.route('/html&css/pages/dashboard/dashboard.html',methods = ['POST'])
def dashboard():
    if request.method == 'POST':
        print(request.form["matric"])
        db = firestore.client()
        users_ref = db.collection(u'Users')
        docs = users_ref.stream()
        temp1 = []
        for doc in docs:
            temp1.append(doc.to_dict()) 
        data = {"Username" : request.form["matric"], "Password" : request.form["password"]}

        if(data in temp1):
            print("success")

            session["name"] = request.form["matric"]


            return redirect(url_for('mainpage'))
        else:
            return render_template('html&css/pages/dashboard/sign-in.html')
           
@app.route('/html&css/pages/dashboard/dashboard.html')   
def mainpage():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    

    return render_template('html&css/pages/dashboard/dashboard.html', subjects=temp, totalAssign= totalAssign,percentage = percentage , resource = resource,name = session.get("name"))
    


@app.route('/html&css/pages/dashboard/KIE3004')
def KIE3004():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []
    print(session.get("name"))

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)


    return render_template('html&css/pages/dashboard/KIE3004.html',subject = temp[0],subjects = temp)

@app.route('/html&css/pages/dashboard/KIE3005')
def KIE3005():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIE3005.html',subject = temp[1],subjects = temp)

@app.route('/html&css/pages/dashboard/KIE3006')
def KIE3006():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIE3006.html',subject = temp[2],subjects = temp)

@app.route('/html&css/pages/dashboard/KIX2001')
def KIX2001():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIX2001.html',subject = temp[3],subjects = temp)

@app.route('/html&css/pages/dashboard/KIX2004')
def KIX2004():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIX2004.html',subject = temp[4],subjects = temp)

@app.route('/html&css/pages/dashboard/KIX3004')
def KIX3004():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIX3004.html',subject = temp[5],subjects = temp)

@app.route('/firebase-messaging-sw.js')
def sw():
    response=make_response(
                     send_from_directory('static',filename='firebase-messaging-sw.js'))
    #change the content header file
    response.headers['Content-Type'] = 'application/javascript'
    return response



if __name__ == "__main__":
    app.run(debug=True)