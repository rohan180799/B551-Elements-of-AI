# utils.py: Utility file for implementing helpful utility functions used by the ML algorithms.
#
# Submitted by: Rohan Mehta -- mehtaro
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

import numpy as np


def euclidean_distance(x1, x2):
    """
    Computes and returns the Euclidean distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    e_dist = np.sqrt(np.sum(np.square(x1 - x2)))
    return e_dist
    # raise NotImplementedError('This function must be implemented by the student.')


def manhattan_distance(x1, x2):
    """
    Computes and returns the Manhattan distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    m_dist = np.abs(x1 - x2).sum()
    return m_dist

    # raise NotImplementedError('This function must be implemented by the student.')


def identity(x, derivative=False):
    """
    Computes and returns the identity activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    if derivative:
        return 1
    else:
        return x
    # raise NotImplementedError('This function must be implemented by the student.')


def sigmoid(x, derivative=False):
    """
    Computes and returns the sigmoid (logistic) activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    sigm = 1 / (1 + np.exp(-x))
    if derivative:
        d_sigm = sigm * (1 - sigm)
        return d_sigm
    else:
        return sigm

    # raise NotImplementedError('This function must be implemented by the student.')


def tanh(x, derivative=False):
    """
    Computes and returns the hyperbolic tangent activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    tan = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

    if derivative:
        dtan = 1 - tan ** 2
        return dtan
    else:
        return tan

    # raise NotImplementedError('This function must be implemented by the student.')


def relu(x, derivative=False):
    """
    Computes and returns the rectified linear unit activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    if derivative:
        if x < 0:
            return 0
        else:
            return 1
    else:
        if x < 0:
            return 0
        else:
            return x
    # raise NotImplementedError('This function must be implemented by the student.')


def softmax(x, derivative=False):
    x = np.clip(x, -1e100, 1e100)
    if not derivative:
        c = np.max(x, axis=1, keepdims=True)
        return np.exp(x - c - np.log(np.sum(np.exp(x - c), axis=1, keepdims=True)))
    else:
        return softmax(x) * (1 - softmax(x))


def cross_entropy(y, p):
    """
    Computes and returns the cross-entropy loss, defined as the negative log-likelihood of a logistic model that returns
    p probabilities for its true class labels y.

    Args:
        y:
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.
        p:
            A numpy array of shape (n_samples, n_outputs) representing the predicted probabilities from the softmax
            output activation function.
    """
    row = p.shape[0]
    sf = softmax(y)
    # if y == 1:
    #     return -np.log(p)
    # else:
    #     return -np.log(1 - p)
    log_likelihood = -np.log(sf[range(row), p])
    loss = np.sum(log_likelihood) / row
    return loss
    # raise NotImplementedError('This function must be implemented by the student.')


# Taken reference from: https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/
def one_hot_encoding(y):
    """
    Converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot
    encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the
    original data.

    Args:
        y: A numpy array of shape (n_samples,) representing the target class values for each sample in the input data.

    Returns:
        A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the input
        data. n_outputs is equal to the number of unique categorical class values in the numpy array y.
    """
    unique_values = np.unique(y)
    mapping = {}
    for idx, ele in enumerate(unique_values):
        mapping[ele] = idx
    one_hot_encode = []
    for i in y:
        zero = list(np.zeros(len(unique_values), dtype=int))
        zero[mapping[i]] = 1
        one_hot_encode.append(zero)
    return one_hot_encode
    # raise NotImplementedError('This function must be implemented by the student.')
