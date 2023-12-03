'''
MODEL-TRAINING
'''

# model_training.py

import joblib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Create a function for the logarithmic transformation
log_transformer = FunctionTransformer(func=np.log1p, inverse_func=np.expm1)

def build_preprocessor(numeric_features, categorical_features):
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('log_transform', log_transformer)
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    return preprocessor

def build_full_pipeline(preprocessor, model):
    return Pipeline([
        ('preprocessor', preprocessor),
        ('model', model)
    ])

def save_model(model, file_path='models/trained_model.pkl'):
    joblib.dump(model, file_path)