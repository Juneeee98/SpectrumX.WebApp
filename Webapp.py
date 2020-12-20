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




            return redirect(url_for('mainpage'))
        else:
            print("failed")
           
@app.route('/html&css/pages/dashboard/dashboard.html')   
def mainpage():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)

    return render_template('html&css/pages/dashboard/dashboard.html', subjects=temp, totalAssign= totalAssign,percentage = percentage , resource = resource)
    


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


    return render_template('html&css/pages/dashboard/KIE3004.html',subject = temp[0])

@app.route('/html&css/pages/dashboard/KIE3005')
def KIE3005():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIE3005.html',subject = temp[1])

@app.route('/html&css/pages/dashboard/KIE3006')
def KIE3006():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIE3006.html',subject = temp[2])

@app.route('/html&css/pages/dashboard/KIX2001')
def KIX2001():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIX2001.html',subject = temp[3])

@app.route('/html&css/pages/dashboard/KIX2004')
def KIX2004():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIX2004.html',subject = temp[4])

@app.route('/html&css/pages/dashboard/KIX3004')
def KIX3004():
    assignSubmitted = []
    assignNo = []
    resource = []
    totalAssign = []
    percentage = []
    temp = []

    getData(session.get("name"),temp, assignNo, assignSubmitted, resource, totalAssign,percentage)
    return render_template('html&css/pages/dashboard/KIX3004.html',subject = temp[5])

@app.route('/firebase-messaging-sw.js')
def sw():
    response=make_response(
                     send_from_directory('static',filename='firebase-messaging-sw.js'))
    #change the content header file
    response.headers['Content-Type'] = 'application/javascript'
    return response


# def drawMonth(month=1):
#     WEEK = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')
#     MONTH = ('January', 'February', 'March', 'April', 'May', 'June',
#              'July', 'August', 'September', 'October', 'November', 'December')

#     # create new blank picture
#     img = Image.new('RGB', size=(1920, 1080), color=(255,255,255))
#     width, height = img.size
#     # rows = 2 titles + 5 rows of days + 2(head + footer)blank
#     # cols = 7 cols of week + 1 blank for left + 3 col for pic
#     rows, cols = 9, len(WEEK) + 4
#     colSpace, rowSpace = width // cols, height // rows

#     # paste your img on the right, 549*1080
#     bgImg = Image.open('static/teddybear.png')
#     bgWidth, _ = bgImg.size
#     img.paste(bgImg, box=(width-bgWidth, 0))

#     # define font and size
#     month_font = r'Montserrat-SemiBold.ttf'
#     title_font = r'Montserrat-Bold.ttf'
#     day_font = r'Montserrat-Medium.ttf'
#     month_size, title_size, day_size = 80, 58, 34

#     draw = ImageDraw.Draw(img)
#     for i in range(len(WEEK) + 1):
#         # draw month title
#         if i == 0:
#             draw.text((colSpace, rowSpace), MONTH[month-1], fill=(0,0,0,), font=ImageFont.truetype(month_font, size=month_size))
#             top = rowSpace // 10
#             draw.line(xy=[(colSpace, rowSpace*2-top * 2), (colSpace*7.5, rowSpace*2-top * 2)], fill=(0,0,0))
#             draw.line(xy=[(colSpace, rowSpace * 2 - top * 1), (colSpace * 7.5, rowSpace * 2 - top * 1)], fill=(0, 0, 0))
#             continue
#         # draw week title
#         draw.text((colSpace*i, rowSpace*2), WEEK[i-1], fill=(0,0,0), font=ImageFont.truetype(title_font, size=title_size))

#     # draw days
#     cal = calendar.Calendar(firstweekday=0)
#     row, col = 3, 1
#     for day in cal.itermonthdays(2019, month):
#         if day > 0:
#             # if weekday, draw with red color
#             if col == 6 or col == 7:
#                 fill = (11, 36, 255)
#             elif col == 2 and row == 4:
#                 fill = (255, 0, 0)
#             elif col == 3 and row == 7:
#                 fill = (255, 0, 0)
#             elif col == 5 and row == 5:
#                 fill = (255, 0, 0)
#             else:
#                 fill = (0, 0, 0)
#             draw.text((colSpace * col + day_size, rowSpace * row), str(day), fill=fill, font=ImageFont.truetype(day_font, size=day_size))
#         col += 1
#         # to a new week
#         if col == 8:
#             col = 1
#             row += 1

#     img.save('static/'+MONTH[month-1] + '.png')



# drawMonth(month=1)

if __name__ == "__main__":
    app.run(debug=True)