#!/usr/bin/env python3
from os import path, DirEntry
import sys
import math
import calendar
from datetime import date
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from inky.inky_uc8159 import Inky, BLACK, WHITE, GREEN, RED, YELLOW, ORANGE, BLUE

inky = Inky()
saturation = 0.5

# font files
titleFontFile = "fonts/Roboto-BlackItalic.ttf"
detailFontFile = "fonts/Roboto-Black.ttf"

# latest update timestamp.
latest_calendar_update = datetime.now() # no need to set current time, just for initial.

class dayInfo:
    def __init__(self, image, date, rect=(0,0, 100,100), borderColor=(0,0,0), fillColor=(255,255,255), events=[]):
        self.image = image
        self.date = date
        self.rect = rect
        self.borderColor = borderColor
        self.fillColor = fillColor
        self.emphsize = False
        self.events = events
        self.specialImage = None

def drawTitle(image, targetDate, calendarRows, boxSize):

    titleOffsetX = 10
    titleOffsetY = 12

    draw = ImageDraw.Draw(image)
    monthString = targetDate.strftime("%B")
    yearString = targetDate.strftime("%Y")
    #weekdayString = targetDate.strftime("%A")
    if date.today() == targetDate:
        monthString = targetDate.strftime("%B %d")


    titleTextAnchor = "la"
    fitstDayOfTheMonth = date(year=targetDate.year, month=targetDate.month, day=1)
    # When the first day of the month starts after wednesday, enlarge the title.

    if fitstDayOfTheMonth.weekday() == 0:
        
        monthFont = ImageFont.truetype(titleFontFile, 56)
        yearFont = ImageFont.truetype(titleFontFile, 32)
        # Calendar move to the top 
        offsetY = 14
        titleOffsetY = 435
        titleOffsetX = 580
        titleTextAnchor = "rd"

        if calendarRows == 4:
            titleOffsetY = 445

        # split it to 2 rows
        draw.text((titleOffsetX, titleOffsetY - 30), monthString, (0,0,0),font=monthFont, anchor=titleTextAnchor)
        draw.text((titleOffsetX, titleOffsetY), yearString, (0,0,0),font=yearFont, anchor=titleTextAnchor)

    elif fitstDayOfTheMonth.weekday() <= 3:
        titleOffsetY = 40
        titleYearOffsetY = 0

        monthFont = ImageFont.truetype(titleFontFile, 32)
        yearFont = ImageFont.truetype(titleFontFile, 24)

        if fitstDayOfTheMonth.weekday() == 2:
            titleOffsetY = 50
            titleYearOffsetY = 10
            monthFont = ImageFont.truetype(titleFontFile, 36)
            yearFont = ImageFont.truetype(titleFontFile, 28)
            

        if fitstDayOfTheMonth.weekday() == 3:
            titleOffsetY = 55
            titleYearOffsetY = 6
            monthFont = ImageFont.truetype(titleFontFile, 46)
            yearFont = ImageFont.truetype(titleFontFile, 28)
            

        # split it to 2 rows
        draw.text((titleOffsetX, titleOffsetY - monthFont.size), monthString, (0,0,0),font=monthFont, anchor=titleTextAnchor)

        
        if fitstDayOfTheMonth.weekday() == 1:
            draw.text((titleOffsetX, titleOffsetY + 56), yearString, (0,0,0),font=yearFont, anchor=titleTextAnchor)
            
            dayFont = ImageFont.truetype(titleFontFile, 56)
            if date.today() == targetDate:
                draw.text((titleOffsetX, titleOffsetY), str(targetDate.day), (0,0,0),font=dayFont, anchor=titleTextAnchor)
        elif fitstDayOfTheMonth.weekday() == 2:
            titlePosX = boxSize[0] * 2
            draw.text((titlePosX, titleOffsetY + 56), yearString, (0,0,0),font=yearFont, anchor="rb")
            
            dayFont = ImageFont.truetype(titleFontFile, 56)
            if date.today() == targetDate:
                draw.text((titleOffsetX, titleOffsetY), str(targetDate.day), (0,0,0),font=dayFont, anchor=titleTextAnchor)
        else:
            titlePosX = boxSize[0] * fitstDayOfTheMonth.weekday()
            draw.text((titlePosX, titleOffsetY + titleYearOffsetY), yearString, (0,0,0),font=yearFont, anchor="ra")

    else:
        fontSize = 48
        titleOffsetX = 20
        # also weeks are 5 row, add more space for the title.
        if calendarRows == 5:
            titleOffsetY = 15
            fontSize = 54
        # when the weeks are 6 row
        if calendarRows == 6:
            titleOffsetY = 0
            fontSize = 54
        
        # split it to 2 rows
        monthFont = ImageFont.truetype(titleFontFile, fontSize)
        yearFont = ImageFont.truetype(titleFontFile, 28)
        draw.text((titleOffsetX, titleOffsetY), monthString, (0,0,0),font=monthFont, anchor=titleTextAnchor)
        draw.text((titleOffsetX, titleOffsetY + 56), yearString, (0,0,0),font=yearFont, anchor=titleTextAnchor)


    

def drawCalendar(image, targetDate=date.today(),borderColor=(0,0,0), fillColor=(255,255,255)):

    # Calc the calendar box(day) size.
    width, height = image.size
    boxWidth = math.floor(width / 8) + 8
    boxHeight = math.floor(height / 7) + 7

    cal = calendar.Calendar()

    # Target year and month 
    targetYear = targetDate.year
    targetMonth = targetDate.month
    weeks = cal.monthdatescalendar(targetYear, targetMonth)

    # Offset calendar from top(Y) and left(X)
    offsetX = 10
    offsetY = 45

    # Check weeks in the calendar, if 6, offset a bit
    # If less than 6 weeks, increase box height.
    if len(weeks) >= 6:
        offsetY = 15
    elif len(weeks) == 4:
        offsetY = 65

        boxHeight = boxHeight + 15 # add more space for 4 row calendar
    else:
        boxHeight = boxHeight + 6

    # when the first day of the month starts on monday, offset to the top.
    if date(targetYear, targetMonth, 1).weekday() == 0:
        offsetY = 10

    # Draw title
    drawTitle(image=image, targetDate=targetDate, calendarRows=len(weeks), boxSize=(boxWidth, boxHeight))

    calendarRow = 0
    for days in weeks:
        xIndex = 0 
        for day in days:
            fillColor = (255, 255, 255) # defaulting the box background color
            eventList = [] # blank..

            info = dayInfo(image, day, (
                boxWidth * xIndex + offsetX, # starting point of x
                boxHeight * calendarRow + offsetY, # starting point of y
                boxWidth * xIndex + offsetX + boxWidth, # ending point of x
                boxHeight * calendarRow + offsetY + boxHeight), # ending point of y
                borderColor=(0,0,0),
                fillColor=fillColor,
                events=eventList)

            if(day.weekday() == 5): # Sat
                info.fillColor = (200, 200, 255)
            if(day.weekday() == 6): # Sun
                info.fillColor = (255, 200, 200)

            if(date.today() == day): # today
                #info.fillColor = (250, 229, 117)
                info.emphsize = True            
            
            # draw box when month is matching to current month.
            if(day.month == targetMonth):

                # check if there is special image for the day. (If you wish to use jpeg format, change here.)

                # image for every month
                pathOfImage = 'images/special_days/'+ day.strftime("%d") + ".png"
                if path.isfile(pathOfImage) == True:
                    info.specialImage = pathOfImage

                # image for specific month
                pathOfImage = 'images/special_days/'+ day.strftime("%m%d") + ".png"
                if path.isfile(pathOfImage) == True:
                    info.specialImage = pathOfImage

                # image for specific year and month
                pathOfImage = 'images/special_days/'+ day.strftime("%Y%m%d") + ".png"
                if path.isfile(pathOfImage) == True:
                    info.specialImage = pathOfImage

                drawBox(info)

            xIndex = xIndex + 1

        calendarRow = calendarRow + 1

def drawBox(info):
    draw = ImageDraw.Draw(info.image, "RGBA")

    # if user put a images under images/special_days/MMDD.png, draw it on the box.
    if info.specialImage != None:
        draw.rectangle(info.rect, fill=(255,255,255,255), outline=(0,0,0,255))
        dayImage = Image.open(info.specialImage)
        # crop the image to adjust the box.
        dayImage = dayImage.crop((0,0, info.rect[2] - info.rect[0] - 1, info.rect[3] - info.rect[1] - 1))
        info.image.paste(dayImage, (info.rect[0] + 1, info.rect[1] + 1))
        return
    
    dayFont = ImageFont.truetype(detailFontFile, 16)
    timeFont = ImageFont.truetype(detailFontFile, 12)
    eventFont = ImageFont.truetype(detailFontFile, 12)

    # if there is no event on the day
    fillColor = (info.fillColor[0], info.fillColor[1], info.fillColor[2], 160)
    if(len(info.events) != 0):
        fillColor = (info.fillColor[0], info.fillColor[1], info.fillColor[2], 255)
    draw.rectangle(info.rect, fill=fillColor, outline=info.borderColor)

    # offset for events
    offsetY = 20
    if(info.emphsize == True):
        draw.rectangle((info.rect[0] + 1, info.rect[1] + 1, info.rect[2] - 1, info.rect[1] + 22), fill=(0,0,0,255), outline=(0,0,0,255))
        draw.text((info.rect[0] + 6, info.rect[1] + 4), str(info.date.day) , (255,255,255,255),font=dayFont)
    else:
        draw.text((info.rect[0] + 6, info.rect[1] + 4), str(info.date.day) , (0,0,0, 255),font=dayFont)
    #print("day : " + str(info.date.day) + " pos x:" + str(info.rect[0]) + " y:" + str(info.rect[1]) + " height " + str(info.rect[2]) + " width " + str(info.rect[3]))
    if(len(info.events) != 0):
        for ev in info.events:
            draw.text((info.rect[0] + 4, info.rect[1] + offsetY), str(ev.start.hour) , (60,60,60),font=timeFont)
            draw.text((info.rect[0] + 4 + 16, info.rect[1] + offsetY), ev.title , (0,0,0),font=eventFont)
            offsetY = offsetY + 16


def update():
    background = Image.open("images/background.jpg")
    foreground = Image.open("images/title_cover.png") # cover top white thing
    background.paste(foreground, (0, 0), foreground)

    # draw calendar
    drawCalendar(background) 
    # if you wish to save the image.
    #background.save("jul.png")


    # update inky impression
    inky.set_image(background, saturation=saturation)
    inky.show()

# generate calendar images for the year, this frunction is just for fun.
def justForFun(year):
    for i in range(1,13):
        targetDate=date(year, i, 28)

        background = Image.open("images/white.png")
        foreground = Image.open("images/title_cover.png") # cover top white thing
        background.paste(foreground, (0, 0), foreground)
        drawCalendar(background, targetDate=targetDate) # open space top left
        month = targetDate.strftime("%B")
        background.save("2021/" + month + ".png")

#justForFun(2021)

# Loop it every day by cron job 
update()