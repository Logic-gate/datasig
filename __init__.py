import os
import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory, Response, jsonify, make_response, stream_with_context
import urllib2
import re
import random
import feedparser
from bs4 import BeautifulSoup
from ascii_graph import Pyasciigraph
from selenium import webdriver
from tabulate import tabulate
import pythonwhois
from functools import wraps
import time
import json
from requests_oauthlib import OAuth1
import requests
import collections
from pytube import YouTube
import base64
import subprocess
import sys
import hashlib
import string
import httplib
import urlparse
import logging
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
from math import floor

#import img2txt
#from PIL import Image
#import cStringIO

#lskjlskdj 


app = Flask(__name__)
#app.config.from_pyfile('flaskapp.cfg')

client = MongoClient('', )
kitc = client['kitcDB']
all_collection = kitc['All_COLLECTION']
msg_collection = kitc['MSG_COLLECTION']
short_collection = kitc['SHORT_COLLECTION']






def error(message, more):
	return {'message': message, "additional info": more} 

@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.errorhandler(404)
def page_not_found(e):
	content = "Ok, if you have an idea for this please pass it along to @m4d_d3v on twitter"
	in_db(all_collection, str(request.__dict__))
	return render_template('content.html', content=content), 404

@app.route("/news")
def NewsLink():
	try:
		browser = urllib2.build_opener()
		browser.addheaders = [('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0')]
		req = browser.open("https://news.google.com/news/section?pz=1&cf=all&topic=n&siidp=5bd18ab44ca49514a94fdccc7c481112cead&ict=ln")
		response = req.read()
		news_link = re.findall(r'url=\"(.*?)\"',response)
		randnumber = random.randint(1, len(news_link) -1)
		return return_json('/news', news_link[randnumber-1])
	except:
		return error('Something went wrong', 'tweet @m4d_d3v..this is very strange')
   # return """
#\033[1;34m """ + news_link[randnumber-1] + """\033[m\n
#"""

@app.route("/me")
def me():
	user_agent = request.headers.get('User-Agent')
	#ip2 = request.headers.get('x-forwarded-for')
	ip1 = request.environ['REMOTE_ADDR']
	try:
		ip2 = request.environ['HTTP_X_FORWARDED_FOR']
		ip = ip1, ip2
	except KeyError:
		ip = ip1
	
	content = {'user_agent': user_agent, 'ip': ip}
	#content = """
#User Agent:"""+ user_agent+ """\n"""+"""
#IP:"""+ ip+""" \n"""
	return return_json('/me', content)

def return_json(origin, content):
	return make_response(jsonify({origin: content}))
	
		#return make_respone('content.html', content=content.replace('\n', '<br/>'))
		

@app.route("/qoute")
def postEduro():
    feed = feedparser.parse('http://www.eduro.com/feed/')
    content = feed['entries'][0]['summary_detail']['value']
    pattern = re.compile('<div>(.*?)</div>', re.I | re.S)
    for i in pattern.findall(content):
        p_remove = re.compile('<p>(.*?)</p>', re.I | re.S)
        for q in p_remove.findall(i):
            pass #q is returned
        auth_remove = re.compile('<p class="author">(.*?)</p>', re.I | re.S)
        for author in auth_remove.findall(i):
            name = re.split('[#&;\d\n]', author) #I am very bad at regexing....
            name_r = filter(None, name)
        content = {"author": name_r[1], "qoute": q}
    return return_json('/qoute', content)
   # return """
#\033[1;31m """ + name_r[1] + """
#\033[1;34m""" + q + """\033[m\n
#"""

@app.route("/scinews")
def postScienceNews():
    '''returns a list of sciencenews article links'''
    feed = feedparser.parse('https://www.sciencenews.org/feeds/headlines.rss')
    link_list = []
    for link in range(len(feed['entries'])):
        link_list.append(feed.entries[link]['link'])
    return return_json('/scinews', link_list)
    #return render_template('list.html', list=link_list)

@app.route("/urban")
def getWord():
	response = urllib2.urlopen("http://www.urbandictionary.com/random.php")
	soup = BeautifulSoup(response.read())
	meaning = soup.find("div", {"class":"meaning"}).text
	word = soup.find("a", {"class":"word"}).text
	example = soup.find("div", {"class":"example"}).text
	content = {"word": word, "meaning": meaning, 'example': example}
	return return_json('/urban', content)
	#return """
#\033[1;31m WORD: \033[1;34m """+ word + """
#\033[1;31m MEANING: \033[1;34m """+ meaning + """
#\033[1;31m EXAMPLE: \033[1;34m """+ example + """\033[m\n
#"""

@app.route("/jokes")
def getJokes():
	response = urllib2.urlopen("http://www.ajokeaday.com/jokes/random")
	soup = BeautifulSoup(response.read(), "html.parser")
	title = soup.find("div", {"class":"jd-body jubilat"}).text
	return return_json('/jokes', title.split('\n')[1])
	#return """
#\033[1;31m JOKE: \033[1;34m """+ title.split('\n')[1]+ """\033[m\n
#"""

@app.route("/weather")
def getLost():
	return return_json('/weather', 'Try http://wttr.in ')

@app.route('/randomnumber')
def randnumber():
	return """
\033[1;31m Random Number (1 - 100000000) """ + str(random.randint(1, 100000000)) + """\033[m\n
"""


@app.route('/hack')
def hack():
	return """
\033[32m	
2687683092
5407103510
2692021165
2856431333
1059244269
5873954412
8115448397
3257235143
1770811632
4033406929
\033[m\n
"""
#0.18051979
@app.route('/solve')
def solve():
	return """
\033[1;31m FIND x \033[1;34m [2, 0.897142857, 0.402432653, x, 0.08097602]
\033[1;31m The prize is 100USD. Send the answer to \033[1;34m @m4d_d3v\033[m\n
"""

@app.route('/pgp')
def keybasepgp():
	response = urllib2.urlopen("https://keybase.io/mad_dev/key.asc")
	return response.read()
	
@app.route('/bitcoin')
def bitcoin():
	return """
\033[1;31m189vBZkLYqRrxQdBvLvspPDGhPBvAhVHqB\033[m\n
"""

@app.route('/secret')
def secret():
	return """
\033[1;31m Dylan Thomas, 1914 - 1953
\033[1;34m
Do not go gentle into that good night,
Old age should burn and rave at close of day;
Rage, rage against the dying of the light.

Though wise men at their end know dark is right,
Because their words had forked no lightning they
Do not go gentle into that good night.

Good men, the last wave by, crying how bright
Their frail deeds might have danced in a green bay,
Rage, rage against the dying of the light.

Wild men who caught and sang the sun in flight,
And learn, too late, they grieved it on its way,
Do not go gentle into that good night.

Grave men, near death, who see with blinding sight
Blind eyes could blaze like meteors and be gay,
Rage, rage against the dying of the light.

And you, my father, there on the sad height,
Curse, bless, me now with your fierce tears, I pray.
Do not go gentle into that good night.
Rage, rage against the dying of the light.\033[m\n
"""


@app.route('/microblog')
def microblog():
	blog = open('blog.txt', 'r')
	return """
\033[1;31mMY MICROBLOG\n\033[1;34m""" + blog.read() + """\033[m\n
"""

@app.route('/twitter/<account>/<tweetid>')
def twitterstat(account, tweetid):
	
	d = webdriver.Remote(command_executor="http://127.6.138.129:15002", desired_capabilities=webdriver.DesiredCapabilities.PHANTOMJS)
	L = "https://twitter.com/"+account+"/status/"+tweetid
	d.get(L)

	soup = BeautifulSoup(d.page_source)
	try:
		tweet = soup.find('p', {'class':'TweetTextSize TweetTextSize--26px js-tweet-text tweet-text'}).text
		retweets = soup.find('ul', {'class':'stats'}).find('li', {'class':'js-stat-count js-stat-retweets stat-count'}).find('a').find('strong').text
		likes = soup.find('ul', {'class':'stats'}).find('li', {'class':'js-stat-count js-stat-favorites stat-count'}).find('a').find('strong').text
		if "," in retweets:
			retweets = retweets.replace(',', '')
		if "," in likes:
			likes = likes.replace(',', '')
		chart = [('retweets', int(retweets)), ('likes', int(likes))]
		gr = Pyasciigraph()
		show = gr.graph(tweet,chart)
		return "\033[1;31m%s\n\033[1;34m%s\n%s\033[m\n" %(show[0], show[2], show[3])
	except:
		try:
			tweet = soup.find('p', {'class':'TweetTextSize TweetTextSize--26px js-tweet-text tweet-text'}).text
			return "\033[1;31m%s\033[m\n" %tweet
		except:
			return "\033[1;31mCould not find tweet\033[m\n"

 

@app.route('/twitter/<account>')
def twitteruser(account):
	d = webdriver.Remote(command_executor="http://127.6.138.129:15002", desired_capabilities=webdriver.DesiredCapabilities.PHANTOMJS)
	L = "https://twitter.com/"+account
	d.get(L)

	soup = BeautifulSoup(d.page_source, "html.parser")
	try:
		try:
			name = soup.find('a', {'class': 'ProfileHeaderCard-nameLink u-textInheritColor js-nav'}).text
			#print 'name'
			if soup.find('span', {'class': 'js-display-url'}):
				desc = soup.find('span', {'class': 'js-display-url'}).text
				#print 'desc'
			else:
				desc = 'Too lazy to write'

			if soup.find('span', {'class':'ProfileHeaderCard-locationText u-dir'}):
				location = soup.find('span', {'class':'ProfileHeaderCard-locationText u-dir'}).text
				#print 'location'
			else: 
				location = 'Probably in Mars'
			if soup.find('span', {'class':'ProfileHeaderCard-joinDateText js-tooltip u-dir'}):
				joined = soup.find('span', {'class':'ProfileHeaderCard-joinDateText js-tooltip u-dir'}).text
				#print 'joined'
			else:
				joined = 'The beginning of time'

			tweets = soup.find('li', {'class': 'ProfileNav-item--tweets'}).find('span', {"class":"ProfileNav-value"}).text
			following = soup.find('li', {'class':'ProfileNav-item--following'}).find('span', {"class":"ProfileNav-value"}).text
			followers = soup.find('li', {'class':'ProfileNav-item--followers'}).find('span', {"class":"ProfileNav-value"}).text
			likes = soup.find('li', {'class':'ProfileNav-item--favorites'}).find('span', {"class":"ProfileNav-value"}).text
		except:
			return 'This is new, note the account and send it to me @m4d_d3v'


		if ',' in tweets.split()[0] or following.split()[0] or followers.split()[0] or likes.split()[0]:
			tweets = tweets.replace(',', '')
			following = following.replace(',', '')
			followers = followers.replace(',', '')
			likes = likes.replace(',', '')

		table = [['Name', name], ['Description', desc], ['Location', location], ['Joined', joined]]

		chart = [('tweets', int(tweets.split()[0])), ('following', int(following.split()[0])), ('followers', int(followers.split()[0])), ('likes', int(likes.split()[0]))]
		gr = Pyasciigraph()

		show = gr.graph('Stats',chart)

		return "\033[1;34m%s\n\n%s\n%s\n%s\n%s\n%s\n\033[m\n" %(tabulate(table), show[0], show[2], show[3], show[4], show[5])
	except:
		return "\033[1;31mCould not find user\033[m\n"





@app.route('/whois', methods = ['GET'])
def whois():
	address = request.args.get('address', None)
	if address is None:
		return return_json('/whois', error('Error in /whois', 'address is missing'))
	#print address
	#name = []
	#data = []
	end = {}
	whois_get = pythonwhois.get_whois(str(address))
	for i in whois_get:
		for ii in whois_get[i]:
			end.update({i:ii})
			#name.append(i)
			#data.append(ii)
			
	#for n, d in zip(name, data):
	#	end.update({n:str(d)})	
		#end.append(n + ':' + str(d))
		
	return return_json('/whois', whois_get)
	#return render_template('index.html', list=end)



@app.route('/short', methods = ['GET'])
def get_url():
	url = request.args.get('url', None)
	try:
		#response = urllib2.urlopen(url)
	
		#response.code == 200:
			#des = response.url
			#print response.geturl()
		des = unshorten_url(url)
		content = {'short_url': url, 'destination': des}
		return return_json('/short', content)
			#return "\033[1;31mShortend URL: \033[1;34mhttp://%s/%s\n\033[1;31mDestination: \033[1;34m%s\033[m\n" %(url, urls, des)
		#else:
		#	return return_json('/short', error('Error in /short', response.code))
			#return '\033[1;34mGot a %s Error code\033[m\n' %response.code
	except:
		return return_json('/short', error('Error in /short', 'code: 404'))
		#return '\033[1;34m Got a 404\033[m\n'


def unshorten_url(url):

    parsed = urlparse.urlparse(url)

    if parsed.scheme == 'https':
        h = httplib.HTTPSConnection(parsed.netloc)
    else:
        h = httplib.HTTPConnection(parsed.netloc)

    resource = parsed.path
    if parsed.query != "": 
        resource += "?" + parsed.query
    h.request('HEAD', resource )
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return unshorten_url(response.getheader('Location')) # changed to process chains of short urls
    else:
        return url


@app.route('/forward', methods = ['GET'])
def forward_url():
	url = request.args.get('url', None)
	return redirect(url, code=302)
	


@app.route('/twitter')
def twitter():
	hel = """
\033[1;31m handle \033[1;34m Show basic information about the user
Example: /twitter/m4d_d3v
\033[1;31m handle/tweetID \033[1;34m Show stats about a tweet
Example: /twitter/ncilla/701787320081633285\033[m\n
"""
	return hel



@app.route('/giphy', methods = ['GET'])
def cat():
	q = request.args.get('q', None)
	data = json.loads(urllib2.urlopen("http://api.giphy.com/v1/gifs/search?q="+q+"&api_key=dc6zaTOxFJmzC").read())
	try:
		l = json.dumps(data)
		f = len(json.loads(l)['data'])  
		gif = json.loads(l)['data'][int(random.randint(1, f))]['images']['fixed_height']['url']
		content = {'url': gif}
		return return_json('/giphy', content)
	except:
		return error('something went wrong', 'Please try again')


@app.route('/gf', methods = ['GET'])
def gf():
	q = request.args.get('q', None)
	data = json.loads(urllib2.urlopen("http://api.giphy.com/v1/gifs/search?q="+q+"&api_key=dc6zaTOxFJmzC").read())
	l = json.dumps(data)
	f = len(json.loads(l)['data'])  
	return redirect(json.loads(l)['data'][int(random.randint(1, f))]['images']['fixed_height']['url'], code=302)



@app.route('/ansi/<link>')
def ansiGen(link):
	file = cStringIO.StringIO(urllib2.urlopen(link).read())
	img = Image.open(file)
	a = img2txt.load_and_resize_image(img, None, 100.0, 1.0)
	pixel = a.load()
	width, height = a.size




	return img2txt.ansi.generate_ANSI_from_pixels(pixel, width, height, None)


client_key    = ""
client_secret = ""
token  = ""
token_secret  = ""


base_twitter_url = "https://api.twitter.com/1.1/"

oauth = OAuth1(client_key, client_secret, token, token_secret)

@app.route('/twitter/following', methods=['GET'])
def get_all_users():
	screen_name = request.args.get('screen_name', None)
	api_url  = "%s/friends/list.json?" % base_twitter_url
	api_url += "screen_name=%s&" % screen_name
	api_url += "count=1000"
	print "sending..."
	response = requests.get(api_url,auth=oauth)
	print "Twitter Auth done."
	if response.status_code == 200:
		print "Starting Fetch Status 200"
		tweets = json.loads(response.content.decode('utf-8'))
		return return_json('/twiiter/following', tweets)
		#return return_json('/twitter/following', 'I am working on a new version')
		#generator = (cell for row in tweets for cell in row)
    	#return Response(str(tweets), mimetype="text/plain", headers={"Content-Disposition": "attachment;filename="+screen_name+"_following.json"})

@app.route('/twitter/followers', methods=['GET'])
def download_followers():
	#screen_name = request.args.get('screen_name', None)
	#followers = get_all_friends_followers(screen_name,"followers")
	#print followers
	#return return_json('/twiiter/followers', followers)
	screen_name = request.args.get('screen_name', None)
	api_url  = "%s/followers/list.json?" % base_twitter_url
	api_url += "screen_name=%s&" % screen_name
	api_url += "count=1000"
	response = requests.get(api_url,auth=oauth)
	if response.status_code == 200:
		tweets = json.loads(response.content.decode('utf-8'))
		return return_json('/twiiter/followers', tweets)
		#return return_json('/twitter/following', 'I am working on a new version')
           # return Response(str(tweets), mimetype="text/plain", headers={"Content-Disposition": "attachment;filename="+screen_name+"_followers.json"})

def get_all_friends_followers(username,relationship_type):
	account_list = []
	next_cursor  = None
	accounts = send_request2(username,relationship_type)
	print 'get'
	non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
	if accounts is not None:
		account_list.extend(accounts['users'])
		while accounts['next_cursor'] != 0 and accounts['next_cursor'] != -1:
			accounts = send_request2(username,relationship_type,accounts['next_cursor'])
			if accounts is not None:
				account_list.extend(accounts['users'])
				#print ("[*] Downloaded %d of type %s" % (len(account_list),relationship_type))
			else:
				break
	return account_list


def send_request2(screen_name,relationship_type,next_cursor=None):
	url = "https://api.twitter.com/1.1/%s/list.json?screen_name=%s&count=5000" % (relationship_type,screen_name)
	if next_cursor is not None:
		url += "&cursor=%s" % next_cursor
		response = requests.get(url,auth=oauth)
		#time.sleep(3)
		if response.status_code == 200:
			result = json.loads(response.content.decode('utf-8'))
			return result
		return None

@app.route('/yt', methods=['GET'])
def youtube():
	forma = request.args.get('format', None)
	res = request.args.get('res', None)
	id = request.args.get('id', None)
	url = "https://www.youtube.com/watch?v=" + id
	try:
		load_video = YouTube(url)
		if forma is None:
			videos = []
			for i, video in enumerate(load_video.get_videos()):
				ext = video.extension
				res = video.resolution
				videos.append('http://ki.tc/yt?id='+id+'&format='+ext+'&res='+res)
			c = {'videos': str(load_video.videos), 'filename': load_video.filename, 'url': url, 'download_links': videos}
			return return_json('/yt', c)
		elif forma is not None:
			add_code = str(random.randint(1, 100000000))
			name = load_video.filename.encode("UTF-8")
			log(name)
			video = load_video.get(forma, res)
			log('video')
			load_video.set_filename(hashlib.sha256(name).hexdigest() + add_code + "_"+request.environ['REMOTE_ADDR'].replace('.', '-'))
			log('hash')
			#load_video.set_filename(hashlib.sha256(load_video.set_filename(base64.b64encode(name) + add_code + request.headers.get('x-forwarded-for'))).hexdigest())
			log(load_video.filename)
			log('hashlib')
			#load_video.set_filename = base64.b64encode(name) + add_code 
			#video.download('/tmp/')
		#	return Response(stream_with_context(generate(video)), mimetype="video/mp4", headers={"Content-Disposition": "attachment;filename="+name+"_"+res+"."+forma})
			v = video.download('/tmp/vid/')
			log('donwloaded')
			g = file('/tmp/vid/'+load_video.filename+'.'+forma)
			try:
				return Response(g, mimetype="video/"+forma, headers={"Content-Disposition": "attachment;filename="+name+"_"+res+"."+forma, 'content-length': str(os.path.getsize('/tmp/vid/'+load_video.filename+'.'+forma))})
			except:
				name = id + "_download"
				return Response(g, mimetype="video/"+forma, headers={"Content-Disposition": "attachment;filename="+name+"_"+res+"."+forma, 'content-length': str(os.path.getsize('/tmp/vid/'+load_video.filename+'.'+forma))})

			'content-length', str(os.path.getsize(FILE_LOCATION))
	except:
		return return_json('/yt',error('caught error', 'make sure the video ID is correct'))


@app.route('/links', methods=['GET'])
def links():
	url = request.args.get('url', None)
	links = []
	resp = urllib2.urlopen(url)
	soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))
	for link in soup.find_all('a', href=True):
		links.append(link['href'])
	c = {'url': url, 'links': links, 'count': len(links)}
	return return_json('/links', c)

@app.route('/img', methods=['GET'])
def img():
	url = request.args.get('url', None)
	images = []
	browser = urllib2.build_opener()
	browser.addheaders = [('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0')]
	urls = browser.open(url)
	soup = BeautifulSoup(urls, from_encoding=urls.info().getparam('charset'))
	for link in soup.find_all('img', src=True):
		images.append(link['src'])
	c = {'url': url, 'images': list(images), 'count': len(images)}
	return return_json('/img', c)

def log(x):
	print x

def in_db(db_name, command):
	db_name.insert({"command": command, "time": datetime.datetime.now()})



@app.route('/m', methods=['POST'])
def creat_msg():
    if not request.json or not 'msg' and 'to' in request.json:
        abort(400)
    msg_id = toBase10(get_random_hash(10))
    admin_id = get_random_hash(21)
    msg_build = {
    	'_id': admin_id,
        'msg': request.json['msg'],
        'to': request.json['to'],
        'from': request.json.get('from', ""),
        'link': "http://ki.tc/m/" + toBase62(msg_id),
        "time": datetime.datetime.now()
    }
    msg_collection.insert({"msg_id": msg_id, "_id": admin_id, "msg_build": msg_build})
    return jsonify({'message': msg_build}), 201


@app.route('/m/<msg_id>', methods=['GET'])
def get_msg(msg_id):
	msg_id10 = toBase10(msg_id)
	access_id = get_random_hash(12)
	try:
		message = msg_collection.find_one({"msg_id": long(msg_id10) })
		access_in = {
		"ip_address": request.environ['REMOTE_ADDR'],
		"access_time": datetime.datetime.now(), 
		'user_agent': request.headers.get('User-Agent'),
		'access_id' : access_id
		}
		msg_collection.update_one({"msg_id": long(msg_id10)}, {"$set":{access_id: access_in}})
		return render_template('msg.html', to=message["msg_build"]["to"], fromm=message["msg_build"]["from"], msg=message["msg_build"]["msg"], time= message["msg_build"]["time"])
		#return jsonify({'msg': message["msg_build"]["msg"], "from": message["msg_build"]["from"], "to": message["msg_build"]["to"], "time": message["msg_build"]["time"]})
	except: 
		content = "Message Not found!"
		in_db(all_collection, str(request.__dict__))
		return render_template('content.html', content=content), 404


@app.route('/m/admin/<admin_id>', methods=['DELETE', 'GET'])
def delete_msg(admin_id):
	if request.method == 'DELETE':
		try:
			if msg_collection.find_one({"_id": admin_id }):
				msg_collection.delete_one({"_id": admin_id })
				return jsonify({'result': True})
			else:
				return jsonify({'result': "Message Not found"})
		except:
			content = "Message Not found!"
			in_db(all_collection, str(request.__dict__))
			return render_template('content.html', content=content), 404
	elif request.method == 'GET':
		try:
			message = msg_collection.find_one({"_id": admin_id })
			#print jsonify({'msg': message["msg_build"]["msg"], "from": message["msg_build"]["from"], "to": message["msg_build"]["to"], "time": message["msg_build"]["time"], 'ip': message["ip_address"], "access_time": message["access_time"], 'user_agent': message["user-agent"]})
			return jsonify(message)
			#return jsonify({'msg': message["msg_build"]["msg"], "from": message["msg_build"]["from"], "to": message["msg_build"]["to"], "time": message["msg_build"]["time"], 'ip': message["ip_address"], "access_time": message["access_time"], 'user_agent': message["user_agent"]}), 201
		except:
			return jsonify({'result': "Message Not found"})
			
	
@app.route('/')
def index():
    
    msg = """
    

  _  _______ _______ _____ 
 | |/ /_   _|__   __/ ____|
 | ' /  | |    | | | |     
 |  <   | |    | | | |     
 | . \ _| |_ _ | | | |____ 
 |_|\_\_____(_)|_|  \_____|
                              0.1.3
                                     

#Known issue in /twitter stats...working on it.

## [0.1.3] - 2017-08-22
### Fixed
- /twitter


## [0.1.3] - 2017-08-16
### Added
- /forward | 302 - redirect to any url
- /links | json - Retrieve all links from a page
- /img | json - Extract all images from a webpage

"""
    return render_template('home_1.html')

@app.route('/', methods=['POST'])
def creat_short_url():
    if not request.json or not 'url' in request.json:
        abort(400)
    url_id = toBase10(get_random_hash(5))
    admin_id = get_random_hash(21)
    url_build = {
    	'_id': admin_id,
        'url': request.json['url'],
        'link': "http://ki.tc/" + toBase62(url_id),
        "time": datetime.datetime.now(),
        "admin_link": "http://ki.tc/url_shortner/" + admin_id
    }
    short_collection.insert({"url_id": url_id, "_id": admin_id, "url_build": url_build})
    return jsonify({'url_short': url_build}), 201


@app.route('/<url_id>', methods=['GET'])
def get_url_short(url_id):
	url_id10 = toBase10(url_id)
	access_id = get_random_hash(12)
	try:
		short = short_collection.find_one({"url_id": long(url_id10) })
		access_in = {
		"ip_address": request.environ['REMOTE_ADDR'],
		"access_time": datetime.datetime.now(), 
		'user_agent': request.headers.get('User-Agent'),
		'access_id' : access_id
		}
		short_collection.update_one({"url_id": long(url_id10)}, {"$set":{str(datetime.datetime.now()) : access_in}})
		url = short["url_build"]["url"]
		return redirect(url, code=302)
		#return render_template('msg.html', to=message["msg_build"]["to"], fromm=message["msg_build"]["from"], msg=message["msg_build"]["msg"], time= message["msg_build"]["time"])
		#return jsonify({'msg': message["msg_build"]["msg"], "from": message["msg_build"]["from"], "to": message["msg_build"]["to"], "time": message["msg_build"]["time"]})
	except: 
		content = "URL Not found!"
		in_db(all_collection, str(request.__dict__))
		return render_template('content.html', content=content), 404


@app.route('/url_shortner/<admin_id>', methods=['DELETE', 'GET'])
def admin_url(admin_id):
	if request.method == 'DELETE':
		try:
			if short_collection.find_one({"_id": admin_id }):
				short_collection.delete_one({"_id": admin_id })
				return jsonify({'result': True})
			else:
				return jsonify({'result': "URL Not found"})
		except:
			content = "URL Not found!"
			in_db(all_collection, str(request.__dict__))
			return render_template('content.html', content=content), 404
	elif request.method == 'GET':
		try:
			message = short_collection.find_one({"_id": admin_id })
			#print jsonify({'msg': message["msg_build"]["msg"], "from": message["msg_build"]["from"], "to": message["msg_build"]["to"], "time": message["msg_build"]["time"], 'ip': message["ip_address"], "access_time": message["access_time"], 'user_agent': message["user-agent"]})
			return jsonify(message)
			#return jsonify({'msg': message["msg_build"]["msg"], "from": message["msg_build"]["from"], "to": message["msg_build"]["to"], "time": message["msg_build"]["time"], 'ip': message["ip_address"], "access_time": message["access_time"], 'user_agent': message["user_agent"]}), 201
		except:
			return jsonify({'result': "URL Not found"})


SIMPLE_CHARS = string.ascii_letters + string.digits

def get_random_string(length=24):
    return ''.join(random.choice(SIMPLE_CHARS) for i in xrange(length))

def get_random_hash(length=24):
    hash = hashlib.sha512()
    hash.update(get_random_string())
    return hash.hexdigest()[:length]



def toBase62(num, b = 62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + string.lowercase + string.uppercase
    r = num % b
    res = base[r];
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res

def toBase10(num, b = 62):
    base = string.digits + string.lowercase + string.uppercase
    limit = len(num)
    res = 0
    for i in xrange(limit):
        res = b * res + base.find(num[i])
    return res

@app.route('/help')
def commands():
	command_list= """

\033[1;31mnews \033[1;34m 
Random news link from Google News 
\033[1;31murban \033[1;34m
Random word from urbandictionary.com
\033[1;31mjokes\033[1;34m 
Random joke from ajokeaday.com
\033[1;31mtwitter\033[1;34m
Random twitter apps
Example: /twitter/m4d_d3v Show basic information about the user
Example: /twitter/ncilla/701787320081633285 Show stats about a tweet
Example: /twitter/following/m4d_d3v get following | json - Works in browser
Example: /twitter/followers/m4d_d3v get followers | json - Works in browser
\033[1;31mrandomnumber\033[1;34m 
Random number
\033[1;31mshort\033[1;34m 
Return the destinationn of a shortend url
Example: /short/tinyurl.com/jhkjh78
Don't add 'HTTP://' it's already defined
\033[1;31mqoute\033[1;34m
Qoute of the day from Eduro\033[m
\033[1;31mme\033[1;34m 
List your user-agent and public IP\033[m
\033[1;31mwhois\033[1;34m 
don't use the IP address
Example: /whois/google.com\033[m
\033[1;31mgiphy \033[1;34m 
Example: /giphy/cat
Returns a random gif of a cat..duh\033[m
\033[1;31mgf \033[1;34m 
Example: /gf/cat
Redirects to a random cat gif..for ease of sharing\033[m\n

"""
	return render_template('help.html')

if __name__ == '__main__':
	app.run()



