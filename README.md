# Instructions on How to Run This Code

To pre-process the data, run:

`python process_data.py total_data.json`

To get the histogram of popularity, run:

`python visualize_data.py data/processed_50_total_data.json`

To see the chi-squared and covariance analysis, run:

`python chi_squared_and_covariance_analysis.py data/processed_50_total_data.json`

To make naive bayes predictions without PCA, run the following command. It may take a while since it's running 5,000 trials. Since we use random holdout we use just one input file.

`python make_naive_bayes_predictions.py <num_trials> data/processed_50_total_data.json`

e.g.

`python make_naive_bayes_predictions.py 500 data/processed_50_total_data.json`

To make naive bayes predictions with PCA, run the following command. `<num_components>` must be a number between 1 and 10. `<filter_c_features>` and `<filter_d_features>` must be 1 or 0. If 1, it only uses the best features from covariance or chi-squared analysis respectively. If you set `<filter_c_features>` to 1 then `<num_components>` is automatically capped at 5.

`python make_naive_bayes_predictions_with_pca.py <num_trials> <num_components> <filter_c_features> <filter_d_features> data/processed_50_total_data.json`

e.g.

`python make_naive_bayes_predictions_with_pca.py 500 10 0 0 data/processed_50_total_data.json`

To graphs of predictions from continuous features when using different PCA configurations, run:

`python pca_graphs.py data/processed_50_total_data.json`
