import json
import sys
import random
import numpy as np
import pprint
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

input_name = sys.argv[1]
input_fp = open(input_name, 'r')
samples = json.load(input_fp)

percent_training = 0.9
num_components = 10

random.seed()

for trial in range(3):
    if trial == 0:
        print('Using all continuous features.\n')
    if trial == 1:
        print('\nNow using acousticness, danceability, energy, instrumentalness, and loudness.\n')
        num_components = 5
    if trial == 2:
        print('\nNow using acousticness, energy, instrumentalness, and loudness.\n')
        num_components = 4
    for sample in samples:
        if trial == 1:
            cont = sample['continuous_features']
            sample['continuous_features'] = [cont[0], cont[1], cont[3], cont[4], cont[6]]
        if trial == 2:
            cont = sample['continuous_features']
            sample['continuous_features'] = [cont[0], cont[2], cont[3], cont[4]]

    training_labels = []
    training_continuous = []
    training_discrete = []

    testing_labels = []
    testing_continuous = []
    testing_discrete = []

    percent_training_popular = 0

    for sample in samples:
        if random.random() < percent_training:
            training_labels.append(sample['label'])
            training_continuous.append(sample['continuous_features'])
            training_discrete.append(sample['discrete_features'])
            if sample['label']:
                percent_training_popular += 1
        else:
            testing_labels.append(sample['label'])
            testing_continuous.append(sample['continuous_features'])
            testing_discrete.append(sample['discrete_features'])

    percent_training_popular /= float(len(training_labels))

    training_continuous = np.array(training_continuous)
    testing_continuous = np.array(testing_continuous)
    pca = PCA(n_components=num_components)
    pca.fit(training_continuous)
    training_continuous = training_continuous.dot(np.transpose(pca.components_))
    testing_continuous = testing_continuous.dot(np.transpose(pca.components_))

    print('PCA Components:')
    pprint.pprint(pca.components_)

    cont_nb = GaussianNB()
    disc_nb = MultinomialNB()

    cont_nb = cont_nb.fit(training_continuous, training_labels)
    disc_nb = disc_nb.fit(training_discrete, training_labels)
    # Combine discrete and continuous by multiplying and handling double prior

    cont_pred = cont_nb.predict_proba(testing_continuous)
    disc_pred = disc_nb.predict_proba(testing_discrete)

    correct = 0
    incorrect = 0

    pred_color = ['orange' for i in range(len(cont_pred))]
    score_color = ['green' for i in range(len(cont_pred))]
    for i in range(len(testing_labels)):
        odds_unpopular = cont_pred[i][0] * disc_pred[i][0] / (1.0 - percent_training_popular)
        odds_popular = cont_pred[i][1] * disc_pred[i][1] / percent_training_popular
        prediction = odds_popular > odds_unpopular
        if prediction == testing_labels[i]:
            correct += 1
        else:
            incorrect += 1
        if (cont_pred[i][0] < cont_pred[i][1]):
            pred_color[i] = 'blue'
        if (cont_pred[i][0] < cont_pred[i][1]) != testing_labels[i]:
            score_color[i] = 'red'
       
    if True:
        plt.rcParams.update({'font.size': 24})
        plt.scatter([c[0] for c in testing_continuous], [c[1] for c in testing_continuous], c=pred_color)
        plt.title('Predictions When Using PCA (First 2 Components)')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.show()
        plt.scatter([c[0] for c in testing_continuous], [c[1] for c in testing_continuous], c=score_color)
        plt.title('Prediction Correctness When Using PCA (First 2 Components)')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.show()
