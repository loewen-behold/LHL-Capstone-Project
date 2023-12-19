# LHL-Capstone-Project: LMS Predictive Analytics

This project focuses on predicting student academic trajectories based on LMS behaviors by using machine learning techniques.

## Table of Contents

- [About](#about)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
  - [Data Preprocessing](#data-preprocessing)
  - [Hyperparameter Tuning](#hyperparameter-tuning)
  - [Model Training](#model-training)
  - [Pre-Prediction Preprocessing](#pre-prediction-preprocessing)
- [Data](#data)
- [Models](#models)
- [API](#api)
  - [Overview](#overview)
  - [Endpoint](#endpoint)
  - [Request Format](#request-format)
  - [Response Format](#response-format)
  - [Example Requests](#example-requests)
  - [Notes](#notes)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## About

The project combines data from the D2L learning management system, student demographics, and grades to predict whether a student is at risk of falling behind.  This can be leveraged by the school's success navigators as an early-warning system tool designed to encourage academic intervention and utlimately, minimize student attrition rates.

## Project Structure

- `notebooks/`: Jupyter notebooks containing EDA, preprocessing, model training, model tuning, and api testing.
- `src/`: Source code files for functions, pre-processors, and GridSearch tuning.
- `data/`: Raw and processed data files.
- `models/`: Saved machine learning models.
- `config/requirements.txt`: Required python packages.
- `api/`: API (app.py) for making predictions.
- `README.md`: Project documentation.

## Getting Started

### Prerequisites

Make sure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/) (version 3.8 or later)
- [pip](https://pip.pypa.io/) (package installer for Python)
- [Jupyter Notebook](https://jupyter.org/install) (for running example notebooks)

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/loewen-behold/LHL-Capstone-Project.git
    ```

2. Navigate to the project directory:

    ```bash
    cd LHL-Capstone-Project
    ```

3. Install project dependencies:

    ```bash
    pip install -r config/requirements.txt
    ```

## Usage

To train the predictive model and make predictions, follow the steps below:

**NOTE:** Steps 1 - 3 can be skipped if the user wishes to use the saved final voting classifier model found in the `models/voting_classifier_best_model.pkl`.  Either load it into a notebook for use, or begin at step 4, which utilizes this model for predictions.

1. **Data Preprocessing**: Use the `src/data_preprocessing.py` module to construct the main dataframe from D2L, demographics, and grades, as well as add all engineered features.

2. **Hyperparameter Tuning**: Utilize the `notebooks/hyperparameter_tuning.ipynb` notebook and `src/hyperparameter_tuning.py` module to tune the classifier models according to the specified scoring metric.

3. **Model Training**: Refer to the `notebooks/model_training.ipynb` Jupyter notebook and `src/model_training.py` module for training the Voting Classifier ML model with the tuned classifier models and the optimal voting weights.

4. **Making Predictions**: Run the `api/app.py` module in the command line.  Then use either the `notebooks/api_testing.ipynb` Jupyter notebook, postman, or any other method of making api calls to make predictions from new student data.  The api utilizes the `src/pre_predict_processing.py` module in order to create synthetic end-of-term values that are then fed into the model for optimized predictions.

## Modules

### Data Preprocessing

- `src/data_preprocessing.py`: Functions for constructing the main dataframe from Excel sheets "d2l", "demographics", and "grades". It also adds all engineered features as well.

### Hyperparameter Tuning

- `src/hyperparameter_tuning.py`: Function for model tuning using GridSearchCV method and custom scoring metrics.

### Model Training

- `src/model_training.py`: Function for custom transformer and model training pipeline.

### Pre-Prediction Preprocessing

- `src/pre_predict_processing.py`: Function to pre-processing mid-term student LMS data (ie n weeks into a semester) into synthetic values to mimic the "end of term" data before using model prediction.

## Data

- Raw data is stored in the `data/raw_data/` directory.
- Processed, clean, and testing data is saved in the `data/processed_data/`.

## Models

- All tuned models (containing the words "best_..._model") and the final voting classifier model are saved in the `models/` directory.

## API

### Overview

The API allows users to make predictions on whether a student is at risk or not based on their partial term Learning Management System (LMS) data. The API endpoint `/predict` accepts POST requests with JSON data.

### Endpoint

- **URL**: `/predict`
- **Method**: `POST`

### Request Format

Send a JSON object in the request body with the following features:

```json
{
    "content_completed": 1,
    "content_required": 7,
    "checklist_completed": 0,
    "quiz_completed": 1,
    "total_quiz_attempts": 3,
    "discussion_post_read": 2,
    "number_of_assignment_submissions": 0,
    "total_time_spent_in_content": 60,
    "number_of_logins_to_the_system": 240,
    "term": "2023F",
    "pseudo_id": 227,
    "pseudo_course": "course_1",
    "total_course_count": 12,
    "course_count_by_term": 6,
    "gender": "M",
    "imm_status": "domestic",
    "age": 21,
    "week": 3
}
```

### Response Format

The API will respond with a JSON object containing the prediction:

#### Not At-Risk

```json
{
    "prediction": "Not At-Risk"
}
```

#### At-Risk

```json
{
    "prediction": "At-Risk"
}
```

### Example Requests

#### Requesting Using Jupyter Notebook:
```python
import requests

url = 'http://localhost:5000/predict'

# Example data for prediction
data = {
    "content_completed": 1,
    "content_required": 7,
    # ... (include other features as needed)
    "week": 3
}

# Send POST request to the API
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.json()}")
```

#### Requesting Using Postman:

1. Call method should be set to "POST"

2. url = 'http://localhost:5000/predict'

3. Under the "Body" tab, click on "raw", paste the following json snippet and make sure to set the datatype to JSON (should be a dropdown beside all of the Body options)
```json
{
    "content_completed": 1,
    "content_required": 7,
    # ... (include other features as needed)
    "week": 3
}
```

4. Click "Send" to see response


### Notes
- Ensure that you replace placeholder data with actual feature values.

## Contributing

Feel free to contribute by submitting issues or pull requests.

## Acknowledgments

- Thank you to **Lambton College** for providing me with the LMS data.
- Special thanks to **Sebastien Lozano-Forero** for curating the data used to train and test the models, and for offering valuable insight and guidance while working through this project.
