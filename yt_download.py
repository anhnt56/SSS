#!/usr/bin/python3
#!G:\Programming\Python\SSS\venv\Scripts

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import youtube_dl
import requests
import pandas
import os

def DownloadVideosFromTitles(los):
	ids = []
	for index, item in enumerate(los):
		vid_id = "https://www.youtube.com/watch?v="+ScrapeVidId(item)
		ids += [vid_id]
	print("Downloading songs....")
	DownloadVideosFromIds(ids)
	print("Downloaded !")

def DownloadVideosFromIds(lov):
	SAVE_PATH = str(os.path.join("G:\Entertain\Music\Spotify"))
	try:
		os.mkdir(SAVE_PATH)
	except:
		print("download folder exists")
	ydl_opts = {
    	'format': 'bestaudio/best',
   		'postprocessors': [{
        		'key': 'FFmpegExtractAudio',
        		'preferredcodec': 'mp3',
        		'preferredquality': '320',
    		}],
		'outtmpl': SAVE_PATH + '\%(title)s.mp3',
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download(lov)

def ScrapeVidId(query):
	print ("Getting video id for: ", query)
	BASIC="http://www.youtube.com/results?search_query="
	URL = (BASIC + query)
	URL.replace(" ", "+")
	page = requests.get(URL)
	session = HTMLSession()
	response = session.get(URL)
	response.html.render(sleep=1)
	soup = BeautifulSoup(response.html.html, "html.parser")

	results = soup.find('a', id="video-title")
	return results['href'].split('/watch?v=')[1]

def __main__():
	data = pandas.read_csv('songs.csv')
	data = data['song names'].tolist()
	print("Found ", len(data), " songs!")
	DownloadVideosFromTitles(data[0:50])
__main__()