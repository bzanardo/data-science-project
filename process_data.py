import json
import pprint
import sys
import numpy as np
import matplotlib.pyplot as plt

input_name = sys.argv[1]  # 'training_data.json'
input_fp = open('data/' + input_name, 'r')
samples = json.load(input_fp)

num_missing_values = 0
for sample in samples:
	if 'acousticness' in sample['values']:
		sample['has_values'] = True
		acousticness = sample['values']['acousticness']
		danceability = sample['values']['danceability']
		duration_ms = sample['values']['duration_ms']
		energy = sample['values']['energy']
		instrumentalness = sample['values']['instrumentalness']
		liveness = sample['values']['liveness']
		loudness = sample['values']['loudness']
		speechiness = sample['values']['speechiness']
		tempo = sample['values']['tempo']
		valence = sample['values']['valence']

		num_artists = len(sample['values']['artists'])
		key = sample['values']['key']
		mode = sample['values']['mode']
		time_signature = sample['values']['time_signature']

		sample['continuous_features'] = [acousticness, danceability, duration_ms, energy,
			instrumentalness, liveness, loudness, speechiness,
			tempo, valence]
		sample['continuous_feature_names'] = ['acousticness', 'danceability', 'duration_ms',
			'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
		sample['discrete_features'] = [num_artists, key, mode, time_signature]
		sample['discrete_feature_names'] = ['num_artists', 'key', 'mode', 'time_signature']
	else:
		num_missing_values += 1
		sample['has_values'] = False

# Filter out the values.

print('A total of ' + str(num_missing_values) + ' songs are missing values.')
samples = [s for s in samples if s['has_values']]

# Normalize each continuous feature with z-score normalization.
continuous_values = np.array([s['continuous_features'] for s in samples])
continuous_values = continuous_values - continuous_values.min(axis=0)
continuous_values = continuous_values / continuous_values.max(axis=0)
for i in range(len(samples)):
	samples[i]['continuous_features'] = continuous_values[i].tolist()

# Label songs as popular/not-popular
popularity = []
for sample in samples:
    popularity.append(sample['values']['popularity'])
popularity.sort()
percentile = 50
percentile_index = int(((len(popularity) - 1) * percentile) / 100)
popular_cutoff = popularity[percentile_index]

# pprint.pprint(samples[0])

num_popular = 0
for sample in samples:
	sample['label'] = sample['values']['popularity'] >= popular_cutoff
	if sample['label']:
		num_popular += 1

print('Num songs (with values): ' + str(len(samples)) + ' Percent popular: ' + str(float(num_popular) / len(samples)))

output_fp = open('data/processed_' + str(percentile) + '_' + input_name, 'w')
json.dump(samples, output_fp)
