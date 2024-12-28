import csv
import math
import operator
import os
from collections import defaultdict

from cx_img.config.configuration import configs


def classify_color_from_rgb(rgb_value):
    package_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    training_data_file = os.path.join(package_root, "resources", "color_detection", "training_dataset",
                                      configs['operation.trainings.color_classification.training_dataset'])
    training_feature_vector = load_dataset(training_data_file)
    k = configs['operation.trainings.color_classification.nearest_neighbors_to_consider']
    neighbors = k_nearest_neighbors(training_feature_vector, rgb_value, k)
    return response_of_neighbors(neighbors)


# Load image feature data to training feature vectors
def load_dataset(file_path):
    training_feature_vector = []
    with open(file_path) as csvfile:
        dataset = list(csv.reader(csvfile))
        for data_row_ind in range(len(dataset)):
            if configs['operation.color_recognition.model.grab_cut.color.active.' + dataset[data_row_ind][-1]]:
                for color_component_ind in range(3):
                    dataset[data_row_ind][color_component_ind] = float(dataset[data_row_ind][color_component_ind])
                training_feature_vector.append(dataset[data_row_ind])
    return training_feature_vector


# get k nearest neighbors
def k_nearest_neighbors(training_feature_vector, test_instance, k):
    distances = []
    length = len(test_instance)
    for x in range(len(training_feature_vector)):
        dist = calculate_euclidean_distance(test_instance, training_feature_vector[x], length)
        distances.append((training_feature_vector[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


# calculation of Euclidean distance
def calculate_euclidean_distance(variable1, variable2, length):
    distance = 0
    for x in range(length):
        distance += pow(variable1[x] - variable2[x], 2)
    return math.sqrt(distance)


# votes of neighbors
def response_of_neighbors(neighbors):
    all_possible_neighbors = defaultdict(int)
    for x in range(len(neighbors)):
        all_possible_neighbors[neighbors[x][-1]] += 1
    sorted_votes = sorted(all_possible_neighbors.items(),
                         key=operator.itemgetter(1), reverse=True)
    return [vote[0] for vote in sorted_votes]


