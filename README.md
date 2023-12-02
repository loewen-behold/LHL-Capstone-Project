# LHL-Capstone-Project: LMS Predictive Analytics

This project focuses on predicting student academic trajectories based on LMS behaviors by using machine learning techniques.

## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Modules](#modules)
  - [Data](#data)
  - [Models](#models)
  - [API](#api)
  - [Configuration](#configuration)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## About

The project combines data from the D2L learning management system, student demographics, and grades to predict whether a student is at risk of falling behind.  This can be leveraged by the school's success navigators as an early-warning system tool designed to encourage academic intervention and utlimately, minimize student attrition rates.

## Project Structure

- `notebooks/`: Jupyter notebooks containing EDA, preprocessing, model training, and model tuning.
- `src/`: Source code files for functions and custom transformers.
- `data/`: Raw and processed data files.
- `models/`: Saved machine learning models.
- `requirements.txt`: Required Python Packages
- `README.md`: Project documentation.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Jupyter Notebook
- Required Python packages (install using `pip install -r requirements.txt`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/loewen-behold/LHL-Capstone-Project.git
   cd LHL-Capstone-Project

## Usage

To train the predictive model and make predictions, follow the steps below:

1. **Data Construction**: Use the `src/data_preprocessing.py` module to construct the main dataframe from D2L, demographics, and grades.

2. **Feature Engineering**: Utilize the `src/feature_engineering.py` module to add engineered features to the dataset.

3. **Preprocessing**: Leverage the custom transformers in `src/preprocessing.py` for data preprocessing.

4. **Model Training**: Refer to the `notebooks/model_training.ipynb` Jupyter notebook for training the machine learning model.

## Modules

### Data Construction

- `src/data_construct.py`: Functions for constructing the main dataframe from D2L, demographics, and grades.

### Feature Engineering

- `src/feature_engineering.py`: Functions for adding engineered features to the dataset.

### Preprocessing

- `src/preprocessing.py`: Custom transformers for data preprocessing.

### Model Training

- `notebooks/model_training.ipynb`: Jupyter notebook for training the machine learning model.

## Data

- Raw data is stored in the `data/` directory.
- Processed data used for training is saved as `processed_data.csv`.

## Models

- Trained Random Forest Classifier is saved in the `models/` directory.

## API (To be Completed)

API functionality to be added.

## Configuration (To be Completed)

Configuration details to be added.

## Contributing

Feel free to contribute by submitting issues or pull requests.

## Acknowledgments

- Thank you to **Lambton College** for providing me with the D2L data.
- Special thanks to **Sebastien Lozano-Forero** for curating the data used to train and test the models, and for offering valuable insight and guidance while working through this project.
