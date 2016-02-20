import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
import urllib2
import re
import random
import feedparser
from bs4 import BeautifulSoup



app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

@app.route('/')
def index():
    return """
\033[1;31m    
 _____    ______  _______  ______   ______  _____  ______  
| | \ \  | |  | |   | |   | |  | | / |       | |  | | ____ 
| |  | | | |__| |   | |   | |__| | '------.  | |  | |  | | 
|_|_/_/  |_|  |_|   |_|   |_|  |_|  ____|_/ _|_|_ |_|__|_|  0.0.1
                                                           
\033[mTry\033[1;31m /help\033[m\n
"""

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.errorhandler(404)
def page_not_found(e):
    return "Ok, if you have an idea for this please pass it along via\033[1;31m @m4d_d3v\033[m on twitter\n", 404

@app.route("/news")
def NewsLink():
    browser = urllib2.build_opener()
    browser.addheaders = [('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0')]
    req = browser.open("https://news.google.com/news/section?pz=1&cf=all&topic=n&siidp=5bd18ab44ca49514a94fdccc7c481112cead&ict=ln")
    response = req.read()
    news_link = re.findall(r'url=\"(.*?)\"',response)
    randnumber = random.randint(1, len(news_link) -1)
    return """
\033[1;34m """ + news_link[randnumber-1] + """\033[m\n
"""
@app.route("/qoute")
def postEduro():
    feed = feedparser.parse('http://www.eduro.com/feed/')
    content = feed['entries'][0]['summary_detail']['value']
    '''
    #Use this to check if the quote date is today...after all, it is qoute of the day
    date = feed['entries'][0]['published'] #RFC 2822 
    post_date = datetime.datetime(*time.strptime(str(date), '%a, %d %b %Y %H:%M:%S +0000')[0:5])
    if post_date.date() == datetime.date.fromtimestamp(time.time()):
        pass
        #print 'Post date was today'
    else:
        post_to_facebook_function
    '''
    pattern = re.compile('<div>(.*?)</div>', re.I | re.S)
    for i in pattern.findall(content):
        p_remove = re.compile('<p>(.*?)</p>', re.I | re.S)
        for q in p_remove.findall(i):
            pass #q is returned
        auth_remove = re.compile('<p class="author">(.*?)</p>', re.I | re.S)
        for author in auth_remove.findall(i):
            name = re.split('[#&;\d\n]', author) #I am very bad at regexing....
            name_r = filter(None, name)
    return """
\033[1;31m """ + name_r[1] + """
\033[1;34m""" + q + """\033[m\n
"""

@app.route("/scinews")
def postScienceNews():
    '''returns a list of sciencenews article links'''
    feed = feedparser.parse('https://www.sciencenews.org/feeds/headlines.rss')
    link_list = []
    for link in range(len(feed['entries'])):
        link_list.append(feed.entries[link]['link'])
    
    return render_template('index.html', list=link_list)

@app.route("/urban")
def getWord():
	response = urllib2.urlopen("http://www.urbandictionary.com/random.php")
	soup = BeautifulSoup(response.read())
	meaning = soup.find("div", {"class":"meaning"}).text
	word = soup.find("a", {"class":"word"}).text
	example = soup.find("div", {"class":"example"}).text

	return """
\033[1;31m WORD: \033[1;34m """+ word + """
\033[1;31m MEANING: \033[1;34m """+ meaning + """
\033[1;31m EXAMPLE: \033[1;34m """+ example + """\033[m\n
"""

@app.route("/jokes")
def getJokes():
	response = urllib2.urlopen("http://www.ajokeaday.com/jokes/random")
	soup = BeautifulSoup(response.read())
	title = soup.find("div", {"class":"team-description"}).text

	return """
\033[1;31m JOKE: \033[1;34m """+ title.split('\n')[2]+ """\033[m\n
"""

@app.route("/weather")
def getLost():
	return """
Hehe...nice catch. Try http://wttr.in it's really cool
"""

@app.route("/changelog")
def changelog():
	return """
# Change Log
All notable changes to this project will be documented in this file.

## 0.0.1 - 2016-02-20
### Added
- /help commands
- /jokes from www.ajokeaday.com
- /urban from urbandictionary.com
- /news from google.com
- /qoute from eduro.com
- /scinews from sciencenews.com [functional but not present in help commands; needs work]
"""

@app.route('/help')
def commands():
	command_list= """
\033[1;31m news \033[1;34m Random news link from Google News 
\033[1;31m urban \033[1;34m Random word from urbandictionary.com
\033[1;31m jokes \033[1;34m Random joke from ajokeaday.com
\033[1;31m qoute \033[1;34m Qoute of the day from Eduro\033[m\n
"""
	return command_list

if __name__ == '__main__':
    app.run()
