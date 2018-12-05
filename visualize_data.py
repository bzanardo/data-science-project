import json
import pprint
import sys
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

input_name = sys.argv[1]
input_fp = open(input_name, 'r')
samples = json.load(input_fp)

popularity = [s['values']['popularity'] for s in samples]

plt.hist(popularity, bins=100, range=(0, 99))
plt.xlabel('Popularity Score')
plt.ylabel('Counts')
plt.title('Popularity Histogram')
plt.show()

continuous = np.array([s['continuous_features'] for s in samples])

pca = PCA(n_components=2)
pca.fit(continuous)
components = continuous.dot(np.transpose(pca.components_))
# outlier_idx = [i for i in range(len(components)) if components[i][0] > 2000000]
# pprint.pprint(samples[outlier_idx[0]])
# print('vs')
# pprint.pprint(samples[0])
plt.scatter([c[0] for c in components], [c[1] for c in components])
plt.title('PCA (2 components) on continuous features')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.show()
