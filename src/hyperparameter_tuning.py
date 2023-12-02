'''
HYPERPARAMETER-TUNING
'''

from sklearn.model_selection import GridSearchCV

def tune_hyperparameters(full_pipeline, X_train, y_train):
    param_grid = {
        'model__n_estimators': [50, 100, 200],
        'model__max_depth': [None, 10, 20, 30],
        # ... (Add more hyperparameters to tune)
    }

    grid_search = GridSearchCV(full_pipeline, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    return grid_search