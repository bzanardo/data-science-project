import json
import sys
import random
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
import statistics as stats
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools

num_trials = int(sys.argv[1])
num_estimators = int(sys.argv[2])
input_name = sys.argv[3]


input_fp = open(input_name, 'r')
samples = json.load(input_fp)

percent_training = 0.9

random.seed()

average_accuracy = 0
average_cont_accuracy = 0
average_disc_accuracy = 0
values = []

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
       
        model_cont = BaggingClassifier(SVC(kernel='rbf', probability=True, gamma=100), n_estimators=num_estimators, warm_start=True)
        model_cont = model_cont.fit(training_continuous, training_labels)
        bagging_cont = model_cont.predict(testing_continuous)
        cont_pred = model_cont.predict_proba(testing_continuous)

        correct = 0
        incorrect = 0

        for i in range(len(testing_labels)):
            odds_unpopular = cont_pred[i][0] / (1.0 - percent_training_popular)
            odds_popular = cont_pred[i][1] / percent_training_popular
            prediction = odds_popular > odds_unpopular
            if prediction == testing_labels[i]:
                correct += 1
            else:
                incorrect += 1
        cont_accuracy = model_cont.score(testing_continuous, testing_labels)
        values.append(cont_accuracy)
        average_cont_accuracy += cont_accuracy #model_cont.score(testing_continuous, testing_labels)

    
    cnf_matrix = confusion_matrix(testing_labels, bagging_cont)

    plt.figure()
    plt.imshow(cnf_matrix, interpolation='nearest')
    plt.title("Confusion Matrix -- SVM with Bagging")
    plt.colorbar()
    classes = ["Positive", "Negative"]
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = 'd'
    thresh = cnf_matrix.max() / 2.
    for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
        plt.text(j, i, format(cnf_matrix[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cnf_matrix[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

    plt.show()


    average_accuracy /= num_trials
    average_cont_accuracy /= num_trials

    print('For SVC w/ Bagging model:')

    print('\t############ average_cont_accuracy #############')
    print('\t' + str(average_cont_accuracy))

    if num_trials > 1:
        std_dev = stats.stdev(values)
        print('\t############ standard deviation #############')
        print('\t' + str(std_dev))


