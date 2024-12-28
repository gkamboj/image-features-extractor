import os
import numpy as np
import cv2
from cx_img.config.configuration import configs


def training():
    package_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    training_dataset_dir = os.path.join(package_root, "resources", "color_detection", "training_dataset")
    training_data_file = os.path.join(training_dataset_dir,
                                      configs['operation.trainings.color_classification.training_dataset'])
    if os.path.exists(training_data_file):
        os.remove(training_data_file)
    for folder in os.listdir(training_dataset_dir):
        folder_path = os.path.join(training_dataset_dir, folder)
        if os.path.isdir(folder_path):
            for color_file in os.listdir(folder_path):
                if color_file != ".DS_Store":
                    color_name = folder
                    image = cv2.imread(os.path.join(training_dataset_dir, folder, color_file))
                    chans = cv2.split(image)
                    colors = ('b', 'g', 'r')
                    features = []
                    feature_data = ''
                    counter = 0
                    for (chan, color) in zip(chans, colors):
                        counter = counter + 1
                        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
                        features.extend(hist)

                        # find the peak pixel values for R, G, and B
                        elem = np.argmax(hist)
                        if counter == 1:
                            blue = str(elem)
                        elif counter == 2:
                            green = str(elem)
                        elif counter == 3:
                            red = str(elem)
                            feature_data = red + ',' + green + ',' + blue

                    with open(training_data_file, 'a') as file:
                        file.write(feature_data + ',' + color_name + '\n')
