import json
import random
import sys
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB

num_trials = int(sys.argv[1])

input_name = sys.argv[2]
input_fp = open(input_name, 'r')
samples = json.load(input_fp)

percent_training = 0.9

random.seed()

average_accuracy = 0
average_cont_accuracy = 0
average_disc_accuracy = 0

for sample in samples:
    cont = sample['continuous_features']
    # sample['continuous_features'] = [cont[0], cont[1], cont[3], cont[4], cont[6]]
    disc = sample['discrete_features']
    # sample['discrete_features'] = [disc[1], disc[2]]

for trial in range(num_trials):
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

    cont_nb = GaussianNB()
    disc_nb = MultinomialNB()

    cont_nb = cont_nb.fit(training_continuous, training_labels)
    disc_nb = disc_nb.fit(training_discrete, training_labels)

    # Combine discrete and continuous by multiplying and handling double prior

    cont_pred = cont_nb.predict_proba(testing_continuous)
    disc_pred = disc_nb.predict_proba(testing_discrete)

    correct = 0
    incorrect = 0

    for i in range(len(testing_labels)):
        odds_unpopular = cont_pred[i][0] * disc_pred[i][0] / (1.0 - percent_training_popular)
        odds_popular = cont_pred[i][1] * disc_pred[i][1] / percent_training_popular
        prediction = odds_popular > odds_unpopular
        if prediction == testing_labels[i]:
            correct += 1
        else:
            incorrect += 1
    average_accuracy += correct / float(correct + incorrect)
    average_cont_accuracy += cont_nb.score(testing_continuous, testing_labels)
    average_disc_accuracy += disc_nb.score(testing_discrete, testing_labels)

average_accuracy /= num_trials
average_cont_accuracy /= num_trials
average_disc_accuracy /= num_trials

print('############ average_accuracy #############')
print(average_accuracy)

print('############ average_cont_accuracy #############')
print(average_cont_accuracy)

print('############ average_disc_accuracy #############')
print(average_disc_accuracy)
