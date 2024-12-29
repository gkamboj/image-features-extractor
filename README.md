# image-features-extractor

This is my first attempt on creating a basic Flask application. This application allows to detect object in any image along with its features like color, etc. Inspirarion behind it was a POC to enable the image based search in the e-commerce website project I worked earlier.


## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Demo and Screenshots](#demo-and-screenshots)
- [Future Improvements](#future-improvements)
- [License](#license)


## Setup Instructions

After cloning the repository, follow these steps to set up the project:

1. **Set Up your development environment**:
   - Download and install JetBrains PyCharm IDE or your preferred IDE.
   - The following instructions will focus on PyCharm, but most IDEs provide similar features.

2. **Open the project**:
   - In PyCharm, navigate to `File -> Open` and select the cloned repository folder.

3. **Set Up a local virtual environment**:
   - Go to `Settings` > `Project: finance-gpt` > `Python Interpreter` > `Add Interpreter`.
   - Choose `Add Local Interpreter` > `Virtualenv Environment`.
     1. Select `Environment` -> `New`.
     2. Set `Base Interpreter` to your installed Python version (e.g., Python 3.x).
     3. Click `OK`.

4. **Install dependencies**:
   Install required dependencies by running the following command in terminal through IDE:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the application**:
   Application can be started by running the following command from the root folder:
   ```bash
   python -m cx_img.app
   ```


## Usage

The application does not include a user interface (UI) but provides two APIs that can be accessed using Postman or any other API client. These APIs are:

1. **Training API**  
   - This API generates a training data file based on [data source color images](https://github.com/gkamboj/image-features-extractor/tree/main/cx_img/resources/color_detection/training_dataset/training_dataset).  
   - It uses color classification to extract and store RGB values for each image in the data source.  
   - Special thanks to [color_recognition by ahmetozlu](https://github.com/ahmetozlu/color_recognition) for inspiring this approach.

2. **Image Classification API**  
   - This API processes input images and returns data about the detected objects, including their confidence scores and features such as color.  
   - The object detection model is based on ResNet40.
   - For color detection, area of main object in the image is identified first through **GrabCut algorithm**. [KNN algorithm](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) is then applied on this object by referencing the training data to determine the color corresponding to the object's RGB values.

### Notes:
- The **Training API** must be executed once during setup to generate the necessary training data for accurate image classification results.  
- To access the Swagger UI for API documentation, navigate to [http://localhost:5001/ui](http://localhost:5001/ui) (or the appropriate port if different).

## Demo and Screenshots
Here are some screenshots showcasing working deployments of the application.
- _Image Classification_ API and sample response:
  <img width="1037" alt="image" src="https://github.com/user-attachments/assets/e020b0dd-ce9e-4bd7-aa6c-a912339676e9" />
  ```
  {
    "result": {
        "attributes": {
            "color": {
                "name": [
                    "black"
                ],
                "rgb": "46,46,46"
            }
        },
        "detection": [
            {
                "confidence": "0.96429",
                "model": "resnet50",
                "name": "running_shoe"
            }
        ]
    },
    "success": true
  }
  ```

- Swagger UI:
  <img width="1625" alt="image" src="https://github.com/user-attachments/assets/7dcc1daa-9070-40bd-9183-f03c617b82ee" />


## Future Improvements
Potential enhancements for future development include:
- Improving color detection accuracy by expanding the dataset with more diverse training images.  
- Adding additional features such as:
  - Object type detection.  
  - Features specific to object types (e.g., collar type, pattern, and color for shirts; brand and color for mobile phones).
- The current use of **ResNet40**, a pretrained model, may limit accuracy for object detection. To achieve higher accuracy, a custom model can be created and trained with a dataset relevant to your usecase.  
- The current approach of using **KNN for color detection** does not perform well for images with multiple colors. A more advanced method is required to handle such scenarios effectively.  

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
