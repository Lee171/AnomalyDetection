import math
import os
import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
from utils.shared_strings import FLIGHT_ROUTES, ATTACKS, FIG_DIR
import pandas as pd


def cosine_similarity(x, y):
    """
    calculate cosine similarity between 2 given vectors
    :param x: vector
    :param y: vector
    :return: cosine similarity
    """
    return dot(x, y) / (norm(x) * norm(y))


def euclidean_distance(x, y):
    """
    calculate the euclidean distance between 2 given vectors
    :param x: vector
    :param y: vector
    :return: euclidean distance
    """
    return np.linalg.norm(x - y)


def anomaly_score(input_vector, output_vector, dist='cosine'):
    """
    calculate the anomaly of single output decoder
    :param x: input vector
    :param y: output vector
    :return: anomaly score based on cosine similarity
    """
    assert len(input_vector) == len(output_vector)
    assert len(input_vector) > 0
    assert dist == 'cosine' or dist == 'euclidean'

    switcher = {
        "cosine": 1 - cosine_similarity(input_vector, output_vector),
        "euclidean_distance": euclidean_distance(input_vector, output_vector)
    }

    return switcher.get(dist, euclidean_distance(input_vector, output_vector))


def anomaly_score_multi(input_vectors, output_vectors):
    """
    calculate the anomaly of a multiple output decoder
    :param input_vectors: list of input vectors
    :param output_vectors: list of output vectors
    :return: anomaly score based on cosine similarity
    """
    sum = 0
    input_length = len(input_vectors)

    assert input_length == len(output_vectors)
    assert input_length > 0

    for i in range(input_length):
        sum += anomaly_score(input_vectors[i], output_vectors[i])

    return sum / input_length


def rolled(list, window_size):
    """
    generator to yield batches of rows from a data frame of <window_size>
    :param list: list
    :param window_size: window size
    :return: batch of rows
    """
    count = 0
    while count <= len(list) - window_size:
        yield list[count: count + window_size]
        count += 1
