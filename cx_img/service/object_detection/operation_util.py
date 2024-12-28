from cx_img.config.configuration import configs
from cx_img.service.object_detection.resnet import detect_object as resnet_detect_object


def detect_object(image):
    result = []
    if configs['operation.object_detection.model.resnet50.active']:
        result += resnet_detect_object(image)
    return result