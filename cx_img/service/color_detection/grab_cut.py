import os

import cv2
import numpy as np

from cx_img.service.color_detection.knn_classifier import classify_color_from_rgb


def get_object_color(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert the image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Define rectangular region around the object to segment
    rect = (50, 50, image.shape[1] - 100, image.shape[0] - 100)

    # Initialize mask for background and foreground
    mask = np.zeros(gray_image.shape[:2], dtype=np.uint8)

    # Initialize background and foreground models
    bgd_model = np.zeros((1, 65), dtype=np.float64)
    fgd_model = np.zeros((1, 65), dtype=np.float64)

    # Run GrabCut algorithm to segment object from the background
    cv2.grabCut(lab_image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    # Create a mask where all probable foreground and certain foreground pixels are set to 1
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Apply the mask to the LAB image
    segmented_image_lab = lab_image * mask2[:, :, np.newaxis]

    # Calculate mean color of the segmented region
    mean_lab_color = cv2.mean(segmented_image_lab, mask=mask2)

    # Convert the mean LAB color to BGR for display
    mean_bgr_color = cv2.cvtColor(np.array([[mean_lab_color[:3]]], dtype=np.uint8), cv2.COLOR_LAB2BGR)[0][0]
    rgb_list = np.array(mean_bgr_color).tolist()[::-1]

    return {
        'rgb': ','.join(str(val) for val in rgb_list),
        'name': classify_color_from_rgb(tuple(rgb_list))
    }
