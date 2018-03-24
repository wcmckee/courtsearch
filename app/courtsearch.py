#app.py

from flask import Flask, request, send_from_directory
import requests
import shutil
import os
import getpass
from urllib.parse import urlparse
import PIL
import json
from PIL import ImageDraw, ImageFont
from PIL import Image
from PIL import ImageDraw
from flask_bootstrap import Bootstrap
import random
import bs4
from requests_html import HTMLSession
import requests_html
import xmltodict
import getpass
import time
import arrow
import crypt
import nltk
from rake_nltk import Rake
import hashlib

myusr = getpass.getuser()
app = Flask(__name__, static_url_path='/static') #create the Flask app
Bootstrap(app)

@app.route('/xml', methods=['GET', 'POST'])
def query_example():
        if request.method == 'POST':  #this block is only entered when the form is submitted
            countrycode = request.form.get('porntag')
            #<input type="radio" name="results" value="10" checked> 10<br>
            vslist = list()




            req = requests.get('http://www.austlii.edu.au/cgi-bin/feed/{}/cases/{}/{}/'.format(countrycode, statecode, courtcode))
            #req = requests.get('http://www.austlii.edu.au/cgi-bin/feed/au/cases/nsw/NSWSC/')
            bsreq = req.text
            xreq = xmltodict.parse(bsreq)
            lenchan = len(xreq['rss']['channel'])
            dalens = len(xreq['rss']['channel']['item'])

            for xr in range(0, dalens):
                #print(xreq['rss']['channel']['item'][xr])
                #print(xreq['rss']['channel']['item'][xr]['title'])
                #print(xreq['rss']['channel']['item'][xr]['link'])
                reqlink = xreq['rss']['channel']['item'][xr]['link']
                reqcourt = requests.get(reqlink)
                reqc = reqcourt.text
                soupcour = bs4.BeautifulSoup(reqc, 'lxml')
                courtit = soupcour.find('title')
                courtext = courtit.text

                repcourt = courtext.replace('[', ',')
                backcourt = repcourt.replace(']', ',')
                newcourt = backcourt.replace('(', ',')
                oldcourt = newcourt.replace(')', ',')

                sosplit = (oldcourt.split(','))
                #print(sosplit[:-4])
                casename = (''.join(sosplit[:-4]))

                casesplit = casename.split('v')
                try:
                    #print(casesplit)
                    vslist.append(casesplit)
            #dicthis = dict({'party1' : (casesplit[0]), 'party2' : casesplit[1]})
                except 'IndexError':
                    pass

                #dicthis = dict({'party1' : (casesplit[0]), 'party2' : casesplit[1]})



        #print(sosplit[-2:-1])
                #casedate =  (''.join(sosplit[-2:-1]))


                #bstxt = bs4.BeautifulSoup(reqsearch.text)

                #sometxt = (bstxt.find_all('li', {'class' : 'multi'}))

                #print(sometxt)



                #for somet in sometxt:
                #    print(somet.text)


            return '''

                    {}


                      '''.format(vslist)

        return '''
                <!DOCTYPE html>
            <html>

            <head>

              <title>Search legal materials</title>
              <script src="https://unpkg.com/vue"></script>
              <script src="node_modules/vue/vue.min.js"></script>
              <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap/dist/css/bootstrap.min.css"/>
              <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue.css"/>
              <meta name="viewport" content="width=device-width, initial-scale=1">
              </head>
              <body>
                <img src="static/header.jpg"><br>
                <h1>Search Recent legal materials API</h1><br>
                <p>Example: au, nsw, NSWSC</p><br>
                <p>This returns party1 and party2 in recent cases.</p>

                <form method="POST">
                  <fieldset>
                    <legend>Search legal materials:</legend>
                      countrycode: <input type="text" name="countrycode"><br>
                      statecode : <input type="text" name="statecode"><br>
                      courtcode : <input type="text" name="courtcode"><br>

                      <input type="submit" value="Submit"><br>
                      </fieldset>
                  </form></body>'''





@app.route('/', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        searchtext = request.form.get('porntag')


        #reqgif = requests.get("https://api.giphy.com/v1/gifs/search?api_key=ee58ff1d10c54fd29ddb0388126c2bcd&q=drugs&limit=25&offset=0&rating=PG-13&lang=en")
        reqhif = requests.get('https://api.giphy.com/v1/gifs/search?api_key=ee58ff1d10c54fd29ddb0388126c2bcd&q={}&limit=25&offset=0&rating=PG-13&lang=en'.format(searchtext))

        reqxm = (reqhif.json())
        rannum = random.randint(0,24)

        gifresult = reqxm['data'][0]['images']['fixed_width']['url']

        img = Image.open('/home/{}/dmgit/app/static/template.jpg'.format(myusr))

        upzero = "I don't always watch porn"


        botzero = "But when I do I watch {}".format(searchtext)

        imageSize = img.size

                # find biggest font size that works
        fontSize = int(imageSize[1]/18)
        font = ImageFont.truetype("/home/{}/Downloads/impact.ttf".format(myusr), fontSize)
        topTextSize = font.getsize(upzero)
        bottomTextSize = font.getsize(botzero)

        fontSize = fontSize - 1
        font = ImageFont.truetype("/home/{}/Downloads/impact.ttf".format(myusr), fontSize)
        topTextSize = font.getsize(upzero)
        bottomTextSize = font.getsize(botzero)

                # find top centered position for top text
        topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
        topTextPositionY = 0
        topTextPosition = (topTextPositionX, topTextPositionY)

                # find bottom centered position for bottom text
        bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
        bottomTextPositionY = imageSize[1] - bottomTextSize[1] -20
        bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

        draw = ImageDraw.Draw(img)

        outlineRange = int(fontSize/15)
        for x in range(-outlineRange, outlineRange+1):
            for y in range(-outlineRange, outlineRange+1):
                draw.text((topTextPosition[0]+x, topTextPosition[1]+y), upzero, (0,0,0), font=font)
                draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), botzero, (0,0,0), font=font)

        draw.text(topTextPosition, upzero, (255,255,255), font=font)
        draw.text(bottomTextPosition, botzero, (255,255,255), font=font)

        img.save("/home/{}/dmgit/app/static/{}.jpg".format(myusr, searchtext))
        #               album_path="me/photos")







        return '''

                <img src="/static/{}.jpg"><br>
                <h1>porntag results</h1><br>
                <img src="{}">
                <h3>Results for<br>
                {}</h3><br>



                  '''.format(searchtext, gifresult, searchtext)

    return '''
            <!DOCTYPE html>
        <html>

        <head>

          <title>Search legal materials</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          </head>
          <body>
            <img src="static/header.jpg"><br>
            <h1>Search legal materials</h1>

            <form method="POST">
              <fieldset>
                <legend>Search legal materials:</legend>
                  porn tag: <input type="text" name="porntag"><br>


                  <input type="submit" value="Submit"><br>
                  </fieldset>
              </form></body>'''

@app.route('/json-example')
def json_example():
    return 'Todo...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #run app in debug mode on port 5000
