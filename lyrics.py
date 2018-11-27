#!/usr/bin/env python3

# Program based on https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62

import json
import pprint
import sys
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup


def scrap_song_url(url):
	page = requests.get(url)
	html = BeautifulSoup(page.text, 'html.parser')
	lyrics = html.find('div', class_='lyrics').get_text()

	return lyrics

def request_song_info(song_title, artist_name):
	base_url = 'https://api.genius.com'
	headers = {'Authorization': 'Bearer ' + 'AukQPwELBzVMPWHBd0oHwCFYBEIGLqOlM1tlcrqxmO32GcirKneEmJlT3aqKSVTP'}
	search_url = base_url + '/search'
	data = {'q': song_title + ' ' + artist_name}
	response = requests.get(search_url, data=data, headers=headers)

	return response

if __name__ == '__main__':
	# Search for matches in the request response

	final = {}
	input_name = 'training_data.json'  # also 'training_data.json'
	input_fp = open('data/' + input_name, 'r')
	samples = json.load(input_fp)
	print(len(samples))
	i=0
	for sample in samples:
		i += 1
		if 'name' in sample['values']:
			song_title = sample['values']['name']
			artist_name = sample['values']['artists'][0]['name']
			print(song_title,artist_name,i)
			response = request_song_info(song_title, artist_name)
			JSON = response.json()
			remote_song_info = None

			for hit in JSON['response']['hits']:
				if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
					remote_song_info = hit
					break

			if remote_song_info:
				song_url = remote_song_info['result']['url']
				final[song_title+'::'+artist_name] = scrap_song_url(song_url)

	output_fp = open('data/lyrics_' + input_name, 'w')
	output_fp.write(json.dumps(final))
	output_fp.close()
