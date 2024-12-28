import cv2
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet import preprocess_input, decode_predictions
from cx_img.config.configuration import configs

def detect_object(image):
    result = []
    try:
        # Load ResNet model pre-trained on ImageNet
        model = ResNet50(weights='imagenet')
        # Preprocess image
        resized_image = cv2.resize(image, (224, 224))

        preprocessed_image = preprocess_input(np.expand_dims(resized_image, axis=0))
        # Predict classes
        predictions = model.predict(preprocessed_image)
        predicted_labels = decode_predictions(predictions)[0]

        top_prediction = predicted_labels[0]
        result.append(create_response(top_prediction[1], top_prediction[2]))

        if len(predicted_labels[0]) > 1 and (top_prediction[2] - predicted_labels[1][2])  <= configs['operation.object_detection.model.resnet50.confidence_diff_threshold']:
            result.append(create_response(predicted_labels[1][1], predicted_labels[1][2]))
    except Exception as e:
        print("Exception while detecting object using Resnet: {0}".format(e))

    return result

def create_response(name, confidence):
    return {
            'name': name,
            'confidence': str(round(confidence, 5)),
            'model': 'resnet50'
        }
