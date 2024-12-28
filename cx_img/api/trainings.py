from cx_img.service.training.color_classifier import training


def color_classification():
    try:
        training()
        success = True
        message = "Successfully created the training data for color classification"
        status_code = 200
    except Exception as e:
        message = "Error while creating the training data for color classification: {}".format(e)
        success = False
        status_code = 500
    result = {'success': success, 'message': message}
    return result, status_code
