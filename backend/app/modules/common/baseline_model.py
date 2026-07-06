import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from typing import Tuple, Any

def train_baseline(df: pd.DataFrame, target_column: str, random_state: int = 42) -> Tuple[Pipeline, str]:
    """
    Trains a baseline Random Forest model on the provided dataset.
    Returns the trained pipeline and the inferred task type ('classification' or 'regression').
    """
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in DataFrame.")

    # Drop rows where target is missing
    df_clean = df.dropna(subset=[target_column]).copy()
    
    if len(df_clean) == 0:
        raise ValueError("No valid rows remaining after dropping missing targets.")

    y = df_clean[target_column]
    X = df_clean.drop(columns=[target_column])

    # Infer task type
    # Simple heuristic: if string/object -> classification
    # If numeric, and unique values < 20 -> classification
    # Otherwise -> regression
    task_type = "regression"
    if y.dtype == 'object' or y.dtype.name == 'category':
        task_type = "classification"
    elif pd.api.types.is_numeric_dtype(y):
        # If float but strictly 0.0 and 1.0, it's classification
        if set(y.dropna().unique()).issubset({0, 1, 0.0, 1.0}):
            task_type = "classification"
        elif pd.api.types.is_integer_dtype(y) and y.nunique() <= 20:
            task_type = "classification"
    
    # Identify column types
    numeric_features = X.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    # Create preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    # Choose model
    if task_type == "classification":
        model = RandomForestClassifier(n_estimators=50, random_state=random_state, max_depth=5)
    else:
        model = RandomForestRegressor(n_estimators=50, random_state=random_state, max_depth=5)

    # Bundle preprocessing and modeling code in a pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('model', model)])

    # Fit model
    clf.fit(X, y)

    return clf, task_type
