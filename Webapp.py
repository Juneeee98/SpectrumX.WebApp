from flask import Flask, render_template, url_for
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

temp = []
assignSubmitted = []
assignNo = []
resource = []
totalAssign = []

Users = firestore_db.collection(u'Users').document("KIE180098").collection("Subjects").stream()

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

def dateFormatter(duedate):
    for i in range(len(duedate)):
        temphol = duedate[i].split(',')
        removeChars = [' AM' , ' PM']
        for j in removeChars:
            temphol[2] = temphol[2].replace(j,'')
        temphol2 = temphol[1].split(' ')
        # temphol2[2] 
        # print(temphol2[2])
        datetime_object = datetime.datetime.strptime(temphol2[2], "%B")
        month_number = datetime_object.month
        temphol[1] = temphol[1].replace(temphol2[2],str(month_number))
    
        temphol1 = temphol[1] + temphol[2]
        temphol1 = temphol1.replace(' ','',1)

        temphol3 = temphol1.split(' ')
        temphol4 = temphol3[0]
        temphol3[0] = temphol3[2]
        temphol3[2] = temphol4
        temphol1 = temphol3[0] +'-'+ temphol3[1] +'-'+ temphol3[2] +' '+ temphol3[3] +':00'
        duedate[i] = temphol1

   
    return duedate

def calculateDurationLeft(duedate):
    durationList = []
    timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start = datetime.datetime.strptime(timenow,'%Y-%m-%d %H:%M:%S')
    for due in duedate:
        ends = datetime.datetime.strptime(due, '%Y-%m-%d %H:%M:%S')
        durationList.append(ends - start)
       
    return durationList


duedate = dateFormatter(duedate = duedate)
durationList = calculateDurationLeft(duedate)
# print(durationList)
# for days in range(len(durationList)):
#     if durationList[days].days < 0 :
#         del durationList[days]

# print(len(durationList))
durationHours = []
durationMinutes = []
durationSec = []
durationDays = []
for duration in durationList:
    durationDays.append(duration.days )
    durationHours.append(math.floor((duration.seconds % (  60 * 60 * 24)) / (  60 * 60)))
    durationMinutes.append(math.floor(duration.seconds % (  60 * 60) / (  60)))
    durationSec.append(math.floor(duration.seconds  %  60 ))
    
overallDone = 0
overallNotDone = 0
for assignSub in assignSubmitted:
    overallDone = assignSub + overallDone
for assignNot in assignNo:
    overallNotDone = assignNot +overallNotDone

# percentageDone = round((overallDone/(overallDone+overallNotDone))* 100)
# print(percentageDone)
labels = 'Submmited' , 'No attempt'
plt.rcParams['font.size'] = 20.0
explode = (0, 0.1)  


sizes = [overallDone,overallNotDone]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90,pctdistance=1.2, labeldistance=0.5,colors = ['lightblue','orange'])
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
fig1.savefig('static/my_plot.png')



percentage = []
for i in range(len(assignSubmitted)):
    percentage.append(round((assignSubmitted[i]/(assignSubmitted[i]+assignNo[i])) * 100))

print(resource)


@app.route('/')
@app.route('/html&css/pages/dashboard/dashboard.html')
def home():
    return render_template('html&css/pages/dashboard/dashboard.html', subjects=temp, totalAssign= totalAssign,percentage = percentage ,resource = resource,durationDays = durationDays , durationHours = durationHours , durationMinutes = durationMinutes , durationSec = durationSec)


@app.route('/html&css/pages/dashboard/KIE3004')
def KIE3004():
    return render_template('html&css/pages/dashboard/KIE3004.html',subject = temp[0])

@app.route('/html&css/pages/dashboard/KIE3005')
def KIE3005():
    return render_template('html&css/pages/dashboard/KIE3005.html',subject = temp[1])

@app.route('/html&css/pages/dashboard/KIE3006')
def KIE3006():
    return render_template('html&css/pages/dashboard/KIE3006.html',subject = temp[2])

@app.route('/html&css/pages/dashboard/KIX2001')
def KIX2001():
    return render_template('html&css/pages/dashboard/KIX2001.html',subject = temp[3])

@app.route('/html&css/pages/dashboard/KIX2004')
def KIX2004():
    return render_template('html&css/pages/dashboard/KIX2004.html',subject = temp[4])

@app.route('/html&css/pages/dashboard/KIX3004')
def KIX3004():
    return render_template('html&css/pages/dashboard/KIX3004.html',subject = temp[5])

@app.route('/firebase-messaging-sw.js')
def sw():
    response=make_response(
                     send_from_directory('static',filename='firebase-messaging-sw.js'))
    #change the content header file
    response.headers['Content-Type'] = 'application/javascript'
    return response


def drawMonth(month=1):
    WEEK = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')
    MONTH = ('January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December')

    # create new blank picture
    img = Image.new('RGB', size=(1920, 1080), color=(255,255,255))
    width, height = img.size
    # rows = 2 titles + 5 rows of days + 2(head + footer)blank
    # cols = 7 cols of week + 1 blank for left + 3 col for pic
    rows, cols = 9, len(WEEK) + 4
    colSpace, rowSpace = width // cols, height // rows

    # paste your img on the right, 549*1080
    bgImg = Image.open('static/teddybear.png')
    bgWidth, _ = bgImg.size
    img.paste(bgImg, box=(width-bgWidth, 0))

    # define font and size
    month_font = r'Montserrat-SemiBold.ttf'
    title_font = r'Montserrat-Bold.ttf'
    day_font = r'Montserrat-Medium.ttf'
    month_size, title_size, day_size = 80, 58, 34

    draw = ImageDraw.Draw(img)
    for i in range(len(WEEK) + 1):
        # draw month title
        if i == 0:
            draw.text((colSpace, rowSpace), MONTH[month-1], fill=(0,0,0,), font=ImageFont.truetype(month_font, size=month_size))
            top = rowSpace // 10
            draw.line(xy=[(colSpace, rowSpace*2-top * 2), (colSpace*7.5, rowSpace*2-top * 2)], fill=(0,0,0))
            draw.line(xy=[(colSpace, rowSpace * 2 - top * 1), (colSpace * 7.5, rowSpace * 2 - top * 1)], fill=(0, 0, 0))
            continue
        # draw week title
        draw.text((colSpace*i, rowSpace*2), WEEK[i-1], fill=(0,0,0), font=ImageFont.truetype(title_font, size=title_size))

    # draw days
    cal = calendar.Calendar(firstweekday=0)
    row, col = 3, 1
    for day in cal.itermonthdays(2019, month):
        if day > 0:
            # if weekday, draw with red color
            if col == 6 or col == 7:
                fill = (11, 36, 255)
            elif col == 2 and row == 4:
                fill = (255, 0, 0)
            elif col == 3 and row == 7:
                fill = (255, 0, 0)
            elif col == 5 and row == 5:
                fill = (255, 0, 0)
            else:
                fill = (0, 0, 0)
            draw.text((colSpace * col + day_size, rowSpace * row), str(day), fill=fill, font=ImageFont.truetype(day_font, size=day_size))
        col += 1
        # to a new week
        if col == 8:
            col = 1
            row += 1

    img.save('static/'+MONTH[month-1] + '.png')



drawMonth(month=1)

if __name__ == "__main__":
    app.run(debug=True)