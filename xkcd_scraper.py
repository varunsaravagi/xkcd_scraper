from bs4 import BeautifulSoup
import urllib
from urllib2 import urlopen
import urllib2
import os.path
import os
import sys

dir_path = '/home/vsaravag/Pictures/xkcd/'
#Get latest file number and initialize url to it
files = sorted([int(f.split('_')[0]) for f in os.listdir(dir_path)], reverse=True)
init_url = "http://www.xkcd.com/"+str(files[0])+'/'
count = 0

# make next url
def make_url(soup):
	global count
	next=soup.find('a', rel='next')
	if next['href'] == '#':
		print 'All comics are downloaded'
		print 'Comics downloaded in this session ', count
		exit()
	else:
		url = "http://www.xkcd.com"+next['href']
		return url

def make_soup(url):
	try:
		html = urlopen(url).read()
	except urllib2.HTTPError as e:
		print str(e) + " " +url
		print "Exit"
		exit()
	return BeautifulSoup(html)

def download(url):
	global count
	try:
		soup = make_soup(url)
	except urllib2.HTTPError as e:
		print str(e) + " " +url
		exit()
	
	img_pane = soup.find(id='comic')
	img_url= img_pane.img['src']
	filename = dir_path+url.split('/')[-2]+'_'+img_url.split('/')[-1]
	if os.path.isfile(filename):
		print 'Image ', filename.split('/')[-1], ' exists'
	else:
		urllib.urlretrieve(img_url,filename)
		print 'Downloaded ', filename
		count += 1
	download(make_url(soup))

download(init_url)
