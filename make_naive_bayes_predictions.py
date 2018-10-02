import json
import random
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB

input_name = 'data/processed_50_testing_data.json'
input_fp = open(input_name, 'r')
samples = json.load(input_fp)

percent_training = 0.9

random.seed()

training_labels = []
training_continuous = []
training_discrete = []

testing_labels = []
testing_continuous = []
testing_discrete = []

for sample in samples:
    if random.random() < percent_training:
        #if (not sample['label']) and random.random() < 0.9:
        #    continue
        training_labels.append(sample['label'])
        training_continuous.append(sample['continuous_features'])
        training_discrete.append(sample['discrete_features'])
    else:
        testing_labels.append(sample['label'])
        testing_continuous.append(sample['continuous_features'])
        testing_discrete.append(sample['discrete_features'])

cont_nb = GaussianNB()
disc_nb = MultinomialNB()

cont_nb = cont_nb.fit(training_continuous, training_labels)
disc_nb = disc_nb.fit(training_discrete, training_labels)

print(testing_labels)

cont_pred = cont_nb.predict_proba(testing_continuous)
disc_pred = disc_nb.predict_proba(testing_discrete)
