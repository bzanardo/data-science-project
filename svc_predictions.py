import json
import random
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier


input_name = 'data/processed_50_total_data.json'
input_fp = open(input_name, 'r')
samples = json.load(input_fp)

percent_training = 0.9

random.seed()

num_trials = 1
average_accuracy = 0
average_cont_accuracy = 0
average_disc_accuracy = 0

for num_components in range(2, 3):
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

        training_continuous = np.array(training_continuous)
        testing_continuous = np.array(testing_continuous)

        svc_model_cont = SVC(probability=True, verbose=True, kernel='rbf')
        #svc_model_disc = SVC(probability=True, verbose=True, kernel='rbf')
        #bagging_model = BaggingClassifier(SVC(kernel='rbf', probability=True))
        
        svc_model_cont = svc_model_cont.fit(training_continuous, training_labels)
        #svc_model_disc = svc_model_disc.fit(training_discrete, training_labels)

        svc_cont = svc_model_cont.predict(testing_continuous)
        #svc_disc = svc_model_disc.predict(testing_discrete)

        svc_cont_pred = svc_model_cont.predict_proba(testing_continuous)
        #svc_disc_pred = svc_model_disc.predict_proba(testing_discrete)

        correct = 0
        incorrect = 0

        for i in range(len(testing_labels)):
            odds_unpopular = svc_cont_pred[i][0] / (1.0 - percent_training_popular)
            odds_popular = svc_cont_pred[i][1] / percent_training_popular
            prediction = odds_popular > odds_unpopular
            if prediction == testing_labels[i]:
                correct += 1
            else:
                incorrect += 1
        average_accuracy += correct / float(correct + incorrect)
        average_cont_accuracy += svc_model_cont.score(testing_continuous, testing_labels)
        #average_disc_accuracy += svc_model_disc.score(testing_discrete, testing_labels)

    average_accuracy /= num_trials
    average_cont_accuracy /= num_trials
    average_disc_accuracy /= num_trials

    print('For SVC model:')
    print('\t############ average_accuracy #############')
    print('\t' + str(average_accuracy))

    print('\t############ average_cont_accuracy #############')
    print('\t' + str(average_cont_accuracy))

    #print('\t############ average_disc_accuracy #############')
    #print('\t' + str(average_disc_accuracy))

