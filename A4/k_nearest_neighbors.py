# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: Rohan Mehta -- mehtaro
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

import numpy as np
from collections import Counter
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._y = y
        # raise NotImplementedError('This function must be implemented by the student.')

# Taken reference from: https://iu.instructure.com/courses/2027431/external_tools/271583
    # and https://medium.com/analytics-vidhya/implementing-k-nearest-neighbours-knn-without-using-scikit-learn-3905b4decc3c
    def predict(self, X):

        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        result = []
        for i in range(len(X)):
            distance = []
            votes = []
            for j in range(len(self._X)):
                dist = euclidean_distance(self._X[j], X[i])
                distance.append([dist, j])
            distance.sort()
            distance = distance[0:self.n_neighbors]
            count_dict = {}
            if self.weights == 'distance':
                unique_values = np.unique(self._y)
                for key in unique_values:
                    count_dict[key] = 0  # initializing to zero
                for dist, index in distance:
                    if dist == 0:
                        count_dict[self._y[index]] += 1
                    else:
                        # this is where we count the inverse of distance as required in the question
                        count_dict[self._y[index]] += 1/dist
                result.append(max(count_dict, key=count_dict.get))
            # computation for self.weights = 'uniform'
            else:
                for a, j in distance:
                    votes.append(self._y[j])
                ans = Counter(votes).most_common(1)[0][0]
                result.append(ans)
        return result
        # raise NotImplementedError('This function must be implemented by the student.')
