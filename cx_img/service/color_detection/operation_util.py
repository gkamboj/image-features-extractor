from cx_img.config.configuration import configs
from cx_img.service.color_detection.grab_cut import get_object_color as grab_cut_detect_color


def detect_color(image):
    result = {}
    if configs['operation.color_recognition.model.grab_cut.active']:
        result['color'] = grab_cut_detect_color(image)
    return result