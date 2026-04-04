"""
svr_model.py
Support Vector Regression (RBF kernel) for Z-Score spread prediction.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score


def train_svr(X_train, y_train, C=50, gamma=0.1, kernel='rbf'):
    """
    Train an SVR model with RBF kernel.

    Args:
        X_train: Training features (scaled).
        y_train: Training targets (scaled).

    Returns:
        Trained SVR model.
    """
    svr = SVR(kernel=kernel, C=C, gamma=gamma)
    svr.fit(X_train, y_train)
    print("SVR (RBF) trained successfully.")
    return svr


def evaluate_svr(model, X_test, y_test, y_scaler):
    """
    Evaluate the SVR model and return predictions + metrics.

    Args:
        model: Trained SVR model.
        X_test: Test features (scaled).
        y_test: Test targets (scaled).
        y_scaler: Fitted MinMaxScaler for inverse transform.

    Returns:
        svr_pred (np.array), metrics (dict)
    """
    svr_pred_scaled = model.predict(X_test)
    svr_pred = y_scaler.inverse_transform(svr_pred_scaled.reshape(-1, 1)).flatten()
    actual = y_scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

    rmse = np.sqrt(mean_squared_error(actual, svr_pred))
    r2 = r2_score(actual, svr_pred)

    print(f"SVR (RBF) → RMSE: {rmse:.4f} | R²: {r2:.4f}")

    plt.figure(figsize=(13, 6))
    plt.plot(actual, color='black', linewidth=2, label='Actual Z-Spread')
    plt.plot(svr_pred, color='tab:orange', alpha=0.8, label='SVR Predicted')
    plt.title("SVR (RBF) — Predicted vs Actual Z-Score Spread")
    plt.xlabel("Time Step")
    plt.ylabel("Z-Score Spread")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('svr_predictions.png')
    plt.show()

    return svr_pred, {'RMSE': rmse, 'R²': r2}


if __name__ == '__main__':
    print("Run from the main notebook pipeline.")
