import numpy as np
from flask import request, jsonify
import io
import cv2

from cx_img.config.configuration import configs
from cx_img.service.color_detection.operation_util import detect_color
from cx_img.service.object_detection.operation_util import detect_object


def detection_and_classification():

    result = {}

    if 'image' not in request.files:
        return create_error_response(False, 'No image provided'), 400

    file = request.files['image']

    if file.filename == '':
        return create_error_response(False, 'No image selected'), 400

    try:
        image_data = file.read()
        image_io = io.BytesIO(image_data)
        image = cv2.imdecode(np.frombuffer(image_io.getvalue(), np.uint8), cv2.IMREAD_COLOR)

        if image is None:
            return create_error_response(False, 'Could not read image data'), 400

        image_copy = image.copy()
        if configs['operation.object_detection.active']: result['detection'] = detect_object(image)
        if configs['operation.color_recognition.active']: result['attributes'] = detect_color(image_copy)

    except Exception as e:
        return create_error_response(False, 'Invalid image file: {0}'.format(e)), 400

    return create_success_response(True, result), 200


def detect_object_and_attributes(image):
    detected_object = "T-shirt"
    attributes = {"color": "blue", "collar_type": "round"}
    return detected_object, attributes


def create_error_response(success, message):
    result = {'success': success, 'message': message}
    return jsonify(result)


def create_success_response(success, result):
    return jsonify({'success': success, 'result': result})
