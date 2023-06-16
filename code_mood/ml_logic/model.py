from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import time
import os
from code.params import *

def train_model(
        X: np.ndarray,
        y: np.ndarray):
    """
    Fit the model and return the fitted model
    """
    model_SVC = SVC(kernel='rbf')

    model_SVC.fit(X, y)

    print(f"✅ Model trained on {len(X)} rows")

    return model_SVC

def evaluated_model(
        X: np.ndarray,
        y: np.ndarray):
    model = train_model()

    print(f"✅ Model evaluated on {len(X)} rows, with average accuracy of {np.round(model.score(X, y)[1], 2)} ")

def save_model(model) -> None:
    """ Persist trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    Save model locally """
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", f"model_saved_{timestamp}")
    model.save(model_path)
