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



reqtag = requests.get('https://api.redtube.com/?data=redtube.Tags.getTagList&output=json')
reqt = (reqtag.json())

taglisz = list()
lentag = len(reqt['tags'])
for lent in range(0, lentag):
    tagterm = (reqt['tags'][lent]['tag']['tag_name'])
    #print(tagterm)
    taglisz.append('<input type="radio" name="tag" value="{}">{}<br>'.format(tagterm, tagterm))

@app.route('/', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        searchtext = request.form.get('tag')

        reqtumblr = requests.get('https://api.tumblr.com/v2/tagged?tag={}&api_key=fuiKNFp9vQFvjLNvx4sUwti4Yb5yGutBN4Xh10LXZhhRKjWlV4'.format(searchtext))
        resptumblr = reqtumblr.json()
        lentumb = len(resptumblr['response'])

        #os.listdir()


        finlist = list()

        for resp in range(0, lentumb):
            try:
                print(resptumblr['response'][resp]['photos'][0]['original_size']['url'])

                finlist.append('<img src="{}">'.format(resptumblr['response'][resp]['photos'][0]['original_size']['url']))

                #r = requests.get(resptumblr['response'][resp]['photos'][0]['original_size']['url'], stream=True)
                #if r.status_code == 200:
                #    with open('/home/pi/dmgit/app/static/{}-{}.jpg'.format(searchtext, resp), 'wb') as f:
                #              r.raw.decode_content = True
                #        shutil.copyfileobj(r.raw, f)


                #os.system("thug /home/pi/memetest/{}.jpg '' ''".format(resp))
            except KeyError:
                pass

        #todayart = os.listdir('/home/pi/memetest/test')

        #finlist = list()
        #for todart in todayart:
        #    finlist.append('<img src="/static/{}/{}"><br><input type="text" name="{}"><br>'.format(searchtext, todart, todart))
        headers = {"X-Mashape-Key": "ASbIsDmx6LmshK1AFZ4ZTzOnuHhTp10VlmpjsnYB5tD15GP9bu","Accept": "text/plain"}

        response = requests.get("https://mashape-community-urban-dictionary.p.mashape.com/define?term={}".format(searchtext), headers=headers)

        taglis = (response.json())
        lenta = len(taglis['list'])
        #print(lenta)
        #print(taglis['list'][lent]['definition'])
        #newdict.update({'tag' : tajs['tag']['tag_name']})
        deflist = list()
        for lent in range(0, lenta):
            #print(taglis['list'][lent]['definition'])
            deflist.append(taglis['list'][lent]['example'] + '<br>')





        #reqgif = requests.get("https://api.giphy.com/v1/gifs/search?api_key=ee58ff1d10c54fd29ddb0388126c2bcd&q=drugs&limit=25&offset=0&rating=PG-13&lang=en")
        reqhif = requests.get('https://api.giphy.com/v1/gifs/search?api_key=ee58ff1d10c54fd29ddb0388126c2bcd&q={}&limit=25&offset=0&rating=R&lang=en'.format(searchtext))

        reqporn = requests.get('https://api.redtube.com/?data=redtube.Videos.searchVideos&output=json&tags[]={}&thumbsize=medium'.format(searchtext))
        reqp = reqporn.json()
        try:
            ranvideo = random.choice(reqp['videos'])
        except KeyError:

            pass

        #someimg = list()
        #lenvid = len(reqp['videos'])
        #for lenr in range(0, lenvid):
        #        print(reqp['videos'][lenr]['video']['title'])
        #          someimg.append()
        #        #print(reqp['videos'][lenr]['video']['title'])
        #        print(reqp['videos'][lenr]['video']['thumb'])


    #print(reqp['videos'][lenr]['video'])

        reqxm = (reqhif.json())
        lenimg = len(reqxm['data'])
        #print(lenimg)
        rannum = random.randint(0,lenimg -1)

        gifresult = reqxm['data'][rannum]['images']['fixed_width']['url']

        





        try:
            return '''

                    <img src="static/{}.jpg"><br>
                    <h1>porntag results</h1><br>
                    <img src="{}">
                    <h3>Results for<br>
                    {}</h3><br>
                    <p>{}</p>
                    <img src="{}"><br>
                    {}<br>
                    {}<br>



                      '''.format(searchtext, gifresult, searchtext, ranvideo['video']['title'], ranvideo['video']['thumb'], [x for x in finlist], [x for x in deflist])
        except UnboundLocalError:
            return '''

                        <img src="/static/{}.jpg"><br>
                        <h1>porntag results</h1><br>
                        <img src="{}">
                        <h3>Results for<br>
                        <img src="{}"><br>
                        {}<br>
                        {}<br>



                          '''.format(searchtext, gifresult, searchtext, [x for x in finlist], [x for x in deflist])



    return '''
            <!DOCTYPE html>
        <html>

        <head>

          <title>Search Porn</title>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          </head>
          <body>
            <img src="static/header.jpg"><br>
            <h1>Search Porn</h1>

            <form method="POST">
              <fieldset>
                <legend>Search porn:</legend>
                  porn tag: <input type="text" name="porntag"><br>

                  {}


                  <input type="submit" value="Submit"><br>
                  </fieldset>
              </form></body>'''.format( [x for x in taglisz])

@app.route('/json-example')
def json_example():
    return 'Todo...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) #run app in debug mode on port 5000
