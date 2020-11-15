from Panel.models import ModelBenchmark
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, auc
import numpy as np
import catboost as ct
import joblib
import pandas as pd
import math
import json


def calculate_metrics_regression(predictions, targets):
    return {
        "mse": mean_squared_error(predictions, targets),
        "rmse": np.sqrt(mean_squared_error(predictions, targets)),
        "mae": mean_absolute_error(predictions, targets),
        "r2_score": r2_score(predictions, targets),
    }


def calculate_metrics_classification(predictions, targets):
    return {
        "accuracy": accuracy_score(predictions, targets),
        "precision": precision_score(predictions, targets),
        "recall": recall_score(predictions, targets),
        "f1_score": f1_score(predictions, targets),
        "auc": auc(predictions, targets)
    }


def get_predictions_catboost(cat, X):
    return cat.predict(X)


def get_predictions_scikit(model, X):
    return model.predict(X)


def get_predictions(model, X):
    if model.model_type == "CatBoost":
        cat = ct.CatBoostRegressor(task_type="CPU", iterations=2000, depth=4)
        cat.load_model(model.model_file_path)
        return get_predictions_catboost(cat, X)
    elif model.model_type == "Scikit-learn":
        jmodel = joblib.load(model.model_file_path)
        return get_predictions_scikit(jmodel, X)


def calculate_metrics(predictions, targets, target_type):
    if target_type == "Regression":
        return calculate_metrics_regression(predictions, targets)
    elif target_type == "Classification":
        return calculate_metrics_classification(predictions, targets)


def create_benchmark(model, dataset):
    if ModelBenchmark.objects.filter(model=model, dataset=dataset).count() > 0:
        return 
    
    json_data = json.loads(open(dataset.scheme_file_path).read())
    dataset_dataframe = pd.read_csv(dataset.dataset_file_path)
    print("JSON DATA: ", json_data)
    X = dataset_dataframe[json_data['X']]
    y = dataset_dataframe[json_data['y']]
    
    predictions = get_predictions(model, X)
    metrics = calculate_metrics(predictions, y, model.target_type)
    mb = ModelBenchmark(model=model, dataset=dataset, metrics=json.dumps(metrics), order=1)
    mb.save()


def check_dataset_dataset_compatibility(dataset1_path, dataset2_scheme):
    dataset1 = pd.read_csv(dataset1_path)
    dataset_scheme_2 = json.loads(open(dataset2_scheme).read())
    return list(dataset1.columns) == list(dataset_scheme_2["X"] + [dataset_scheme_2["y"]])


def check_model_dataset_compatibility(model, dataset):
    model_scheme = json.loads(open(model.scheme_file_path).read())
    dataset_scheme = json.loads(open(dataset.scheme_file_path).read())
    return len(dataset_scheme["X"]) == model_scheme["features_shape"]
