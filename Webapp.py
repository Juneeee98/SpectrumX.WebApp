from flask import Flask, render_template, url_for
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import calendar

load_dotenv()
cred = credentials.Certificate(os.getenv("serviceAccountKey"))
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

app = Flask(__name__)

temp = []
assignSubmitted = []
assignNo = []

Users = firestore_db.collection(u'Users').document("KIE180098").collection("Subjects").stream()

for user in Users:
    temp.append(user.to_dict()) 

i = -1
for subject in temp:
    i= i + 1
    assignNo.append(0)
    assignSubmitted.append(0)
    for subTopic in subject["subTopic"]:
        print(subTopic)
        if "Submitted" in str(subTopic):
            assignSubmitted[i] = assignSubmitted[i] + 1
        elif "No attempt" in str(subTopic):
            assignNo[i] = assignNo[i] + 1

labels = 'Submmited' , 'No attempt'
explode = (0, 0.1)  

for i in range(len(assignSubmitted)):
    sizes = [assignSubmitted[i],assignNo[i]]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig1.savefig('static/my_plot' + str(i) + '.png')





@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', subjects=temp)



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
                print(row)
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