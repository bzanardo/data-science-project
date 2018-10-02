import json
import pprint

input_name = 'testing_data.json'
input_fp = open(input_name, 'r')
samples = json.load(input_fp)

# Label songs as popular/not-popular
popularity = []
for sample in samples:
    popularity.append(sample['values']['popularity'])
popularity.sort()
percentile = 90
percentile_index = int(((len(popularity) - 1) * percentile) / 100)
popular_cutoff = popularity[percentile_index]

for sample in samples:
    sample['values']['popular'] = sample['values']['popularity'] >= popular_cutoff

output_fp = open('labeled_' + input_name, 'w')
json.dump(samples, output_fp)
