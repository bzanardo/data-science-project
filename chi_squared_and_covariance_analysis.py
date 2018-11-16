import json
import pprint
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

input_name = sys.argv[1]
input_fp = open(input_name, 'r')
samples = json.load(input_fp)

popularity_num = [s['values']['popularity'] for s in samples]
popularity_flag = [1 if s['label'] else 0 for s in samples]

discrete_values = [s['discrete_features'] for s in samples]
continuous_values = [s['continuous_features'] for s in samples]

print('\n#################### CHI SQUARED ######################\n')

for feature_idx in range(len(discrete_values[0])):
	feature_values = [d[feature_idx] for d in discrete_values]
	fv_pop_counts = {}
	col_total = [0, 0]
	total = 0
	for i in range(len(feature_values)):
		if feature_values[i] not in fv_pop_counts:
			fv_pop_counts[feature_values[i]] = [0, 0]
		fv_pop_counts[feature_values[i]][popularity_flag[i]] += 1
		col_total[popularity_flag[i]] += 1
		total += 1
	obs_vector = []
	exp_vector = []
	for fv, pop_counts in fv_pop_counts.items():
		if pop_counts[0] == 0:
			pop_counts[0] = 0.001
		if pop_counts[1] == 0:
			pop_counts[1] = 0.001
		obs_vector.append(pop_counts)
		exp_vector.append(
			[(pop_counts[0] * col_total[0]) / float(total),
			 (pop_counts[1] * col_total[1]) / float(total)])
	print('Result for feature ' + str(feature_idx) + ' which has the following values:')
	pprint.pprint([k for k in fv_pop_counts])
	# pprint.pprint(obs_vector)
	# pprint.pprint(exp_vector)
	result = stats.chisquare(obs_vector, exp_vector)
	print(result)

print('\n#################### COVARIANCE ######################\n')
for feature_idx in range(len(continuous_values[0])):
	feature_values = [c[feature_idx] for c in continuous_values]
	print('Covariance between feature ' + str(feature_idx) + ' and popularity: ' + str(np.cov(feature_values, popularity_num)[0][1])) 
