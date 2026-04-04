"""
rf_model.py
Random Forest model for Z-Score spread prediction.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def train_random_forest(X_train, y_train,
                        n_estimators=300, max_depth=10, random_state=42):
    """
    Train a Random Forest regressor.

    Args:
        X_train: Training features (scaled).
        y_train: Training targets (scaled).

    Returns:
        Trained RandomForestRegressor model.
    """
    rf = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    print("Random Forest trained successfully.")
    return rf


def evaluate_random_forest(model, X_test, y_test, y_scaler):
    """
    Evaluate the Random Forest model and return predictions + metrics.

    Args:
        model: Trained RF model.
        X_test: Test features (scaled).
        y_test: Test targets (scaled).
        y_scaler: Fitted MinMaxScaler for inverse transform.

    Returns:
        rf_pred (np.array), metrics (dict)
    """
    rf_pred_scaled = model.predict(X_test)
    rf_pred = y_scaler.inverse_transform(rf_pred_scaled.reshape(-1, 1)).flatten()
    actual = y_scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

    rmse = np.sqrt(mean_squared_error(actual, rf_pred))
    r2 = r2_score(actual, rf_pred)

    print(f"Random Forest → RMSE: {rmse:.4f} | R²: {r2:.4f}")

    plt.figure(figsize=(13, 6))
    plt.plot(actual, color='black', linewidth=2, label='Actual Z-Spread')
    plt.plot(rf_pred, color='tab:blue', alpha=0.8, label='RF Predicted')
    plt.title("Random Forest — Predicted vs Actual Z-Score Spread")
    plt.xlabel("Time Step")
    plt.ylabel("Z-Score Spread")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('rf_predictions.png')
    plt.show()

    return rf_pred, {'RMSE': rmse, 'R²': r2}


if __name__ == '__main__':
    print("Run from the main notebook pipeline.")
