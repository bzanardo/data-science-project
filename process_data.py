import json
import pprint

input_name = 'testing_data.json'
input_fp = open('data/' + input_name, 'r')
samples = json.load(input_fp)

# Label songs as popular/not-popular
popularity = []
for sample in samples:
    popularity.append(sample['values']['popularity'])
popularity.sort()
percentile = 90
percentile_index = int(((len(popularity) - 1) * percentile) / 100)
popular_cutoff = popularity[percentile_index]

# pprint.pprint(samples[0])

for sample in samples:
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
    sample['discrete_features'] = [num_artists, key, mode, time_signature]
    sample['label'] = sample['values']['popularity'] >= popular_cutoff

output_fp = open('data/processed_' + str(percentile) + '_' + input_name, 'w')
json.dump(samples, output_fp)
