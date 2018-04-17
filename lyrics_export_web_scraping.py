#Import libraries
import csv
from datetime import datetime
import re
import urllib2
from bs4 import BeautifulSoup
import codecs
import sys
import string

# Variables init
url_website = 'http://paroles2chansons.lemonde.fr/paroles-'
url_artist_name = 'damien-saez'
url_albums_list = ['jours-etranges'
					,'katagena'
					,'debbie'
					,'varsovie-l-alhambra-paris'
					,'a-lovers-prayer'
					,'j-accuse'
					,'messina'
					,'miami'
					,'le-manifeste-l-oiseau-liberte-prelude-acte-ii'
					,'god-blesse'
					,'lulu'
				]
url_part_album = '/album-'
url_part_paroles = '/paroles-'	
artist_name = url_artist_name.replace('-',' ').title()
date_timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
output_file_name = 'export_' + url_artist_name + '_' + date_timestamp + '.csv'


# Each album page is parsed to retrieve the link to each song page				
for url_album in url_albums_list:

	# Define the album name
	album_name = url_album.replace('-',' ').title()
	
	# Build the album url
	url = url_website + url_artist_name + url_part_album + url_album + '.html'
	
	# Query the website and return the html to the variable 'album_page'
	album_page = urllib2.urlopen(url)

	# Parse the html in the 'album_page' variable, and store it in Beautiful Soup format
	soup_album = BeautifulSoup(album_page, 'html.parser')

	# Retrieve song page url from tag a, class 'link grey font-small'
	album_page_song_urls = soup_album.find_all("a", class_="link grey font-small")
	
	# Only links related to the artist songs are retrieved
	for album_page_song_url in album_page_song_urls:
		matchObj = re.search(url_artist_name, album_page_song_url.get('href'))
		if matchObj:
			if  album_page_song_url.get('href') <> url_website + url_artist_name + url_part_paroles + '.html':
				print album_page_song_url.get('href')
				song_url = album_page_song_url.get('href')
				
				# Query the website and return the html to the variable 'song_page'
				song_page = urllib2.urlopen(song_url)

				# Parse the html in the 'song_page' variable, and store it in Beautiful Soup format
				soup_song = BeautifulSoup(song_page, 'html.parser')
				
				# Retrieve and format song title from tag H1
				soup_song_tag_h1 = soup_song.find('h1', attrs={'class': 'uppercase font-24'})
				song_title = soup_song_tag_h1.text[soup_song_tag_h1.text.find(' ')+1:soup_song_tag_h1.text.find(artist_name)-5]
				print song_title.encode('utf-8', 'replace')

				# Retrieve song lyrics from tag div, class 'border block-spacing-medium text-center'
				soup_song_tag_div = soup_song.find('div', attrs={'class': 'border block-spacing-medium text-center'})
				song_lyrics_raw = soup_song_tag_div.text
				
				# Cleaning tag div containing lyrics
				song_lyrics_cleaned = song_lyrics_raw.replace("googletag.cmd.push(function() { googletag.display('container-middle-lyrics'); });","").replace("/* ringtone - Above Lyrics */","").replace("/* ringtone - Below Lyrics */","").replace("\t","").replace("\r\n"," ").rstrip("\r\n")
				song_lyrics = re.sub(".*\((.*)\).*", "", song_lyrics_cleaned).strip().replace("\n", " ")

				# Finalising the line containing the song title + lyrics
				song_line = '"' + album_name + '";"' + song_title + '";"' + song_lyrics + '"' + '\r'
			
				# Line stored into a text file
				output_file = open(output_file_name,'a')
				output_file.write(song_line.encode('utf-8', 'replace'))
				output_file.close()
