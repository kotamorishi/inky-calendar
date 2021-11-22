#!/usr/bin/env python3

import sys
import math
import calendar
from datetime import date

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from inky.inky_uc8159 import Inky

inky = Inky()
saturation = 0.6

class dayInfo:
    def __init__(self, image, date, rect=(0,0, 100,100), borderColor=(0,0,0), fillColor=(255,255,255)):
        self.image = image
        self.date = date
        self.rect = rect
        self.borderColor = borderColor
        self.fillColor = fillColor
        self.emphsize = False
        self.scheduleItems = []
    def addList(shortText, longText):
        pass

def drawCalendar(image, borderColor=(0,0,0), fillColor=(255,255,255)):

    width, height = image.size
    boxWidth = math.floor(width / 8) + 5
    boxHeight = math.floor(height / 7) + 6

    c = calendar.TextCalendar(calendar.MONDAY)
    today = date.today()
    c.prmonth(today.year, today.month)

    draw = ImageDraw.Draw(image)
    dateFont = ImageFont.truetype("fonts/Roboto-BlackItalic.ttf", 36)
    weekDayFont = ImageFont.truetype("fonts/Roboto-BlackItalic.ttf", 16)
    dateString = today.strftime("%B %d")
    weekdayString = today.strftime("%A")

    draw.text((20, 15), dateString, (50,50,50),font=dateFont)
    #draw.text((width - 140, 20), weekdayString, (50,50,50),font=weekDayFont)

    cal = calendar.Calendar()
    weeks = cal.monthdatescalendar(today.year, today.month)
    offsetX = 20
    offsetY = 60
    calendarRow = 0
    for days in weeks:
        xIndex = 0 
        for day in days:
            fillColor = (255, 255, 255) # defaulting the box background color
            info = dayInfo(image, day, (
                boxWidth * xIndex + offsetX, # starting point of x
                boxHeight * calendarRow + offsetY, # starting point of y
                boxWidth * xIndex + offsetX + boxWidth, # ending point of x
                boxHeight * calendarRow + offsetY + boxHeight), # ending point of y
                borderColor=(0,0,0),
                fillColor=fillColor)

            if(day.weekday() == 5): # Sat
                info.fillColor = (228, 228, 255)
            if(day.weekday() == 6): # Sun
                info.fillColor = (250, 200, 200)

            if(today == day): # today
                info.fillColor = (250, 229, 117)
                info.emphsize = True            
            
            if(day.month == today.month):
                # draw box when month is matching to current month.
                drawBox(info)

            xIndex = xIndex + 1

        calendarRow = calendarRow + 1

def drawBox(info):
    draw = ImageDraw.Draw(info.image)
    font = ImageFont.truetype("fonts/Roboto-Medium.ttf", 14)
    draw.rectangle(info.rect, fill=info.fillColor, outline=info.borderColor)
    #if(info.emphsize == True):
    #    draw.ellipse((info.rect[0] + 1, info.rect[1] + 1, info.rect[0] + 2 + 20, info.rect[1] + 2 + 20), fill = 'red', outline ='red')

    draw.text((info.rect[0] + 4, info.rect[1] + 4), str(info.date.day) , (60,60,60),font=font)
    #print("day : " + str(info.date.day) + " pos x:" + str(info.rect[0]) + " y:" + str(info.rect[1]) + " height " + str(info.rect[2]) + " width " + str(info.rect[3]))


background = Image.open("background.jpg")
foreground = Image.open("title_cover.png")
background.paste(foreground, (0, 0), foreground)

drawCalendar(background)
background.save("temp.png")

inky.set_image(background, saturation=saturation)
inky.show()
