'''
HYPERPARAMETER-TUNING
'''

from sklearn.model_selection import GridSearchCV

def tune_hyperparameters(model, param_grid, X_train, y_train, scoring='recall'):
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring=scoring, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    return grid_search