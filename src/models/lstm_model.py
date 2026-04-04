"""
lstm_model.py
LSTM model for Z-Score spread prediction with 60-step lookback.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
except ImportError:
    print("TensorFlow not installed. LSTM model unavailable.")


def create_sequences(X_data, y_data, time_steps=60):
    """
    Create 3D sequences for LSTM input.

    Args:
        X_data: Feature array (scaled).
        y_data: Target array (scaled).
        time_steps: Lookback window size.

    Returns:
        Xs (np.array), ys (np.array)
    """
    Xs, ys = [], []
    for i in range(len(X_data) - time_steps):
        Xs.append(X_data[i:(i + time_steps)])
        ys.append(y_data[i + time_steps])
    return np.array(Xs), np.array(ys)


def build_lstm(input_shape):
    """
    Build and compile the LSTM model.

    Args:
        input_shape: Tuple (lookback, n_features).

    Returns:
        Compiled Keras Sequential model.
    """
    model = Sequential([
        LSTM(64, input_shape=input_shape, return_sequences=False),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.0005), loss='huber')
    print(model.summary())
    return model


def train_lstm(model, trainX, trainY, epochs=60, batch_size=32):
    """
    Train the LSTM model with early stopping.

    Returns:
        Trained model and training history.
    """
    es = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    lr_sched = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-5)

    history = model.fit(
        trainX, trainY,
        validation_split=0.1,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[es, lr_sched],
        verbose=1
    )
    print("LSTM training complete.")
    return model, history


def evaluate_lstm(model, testX, testY, y_scaler):
    """
    Evaluate LSTM model and return predictions + metrics.

    Returns:
        lstm_pred (np.array), metrics (dict)
    """
    pred_scaled = model.predict(testX).flatten()
    lstm_pred = y_scaler.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()
    actual = y_scaler.inverse_transform(testY.reshape(-1, 1)).flatten()

    rmse = np.sqrt(mean_squared_error(actual, lstm_pred))
    r2 = r2_score(actual, lstm_pred)

    print(f"LSTM → RMSE: {rmse:.4f} | R²: {r2:.4f}")

    plt.figure(figsize=(13, 6))
    plt.plot(actual, color='black', linewidth=2, label='Actual Z-Spread')
    plt.plot(lstm_pred, color='red', alpha=0.7, label='LSTM Predicted')
    plt.title("LSTM — Predicted vs Actual Z-Score Spread")
    plt.xlabel("Time Step")
    plt.ylabel("Z-Score Spread")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('lstm_predictions.png')
    plt.show()

    return lstm_pred, {'RMSE': rmse, 'R²': r2}


if __name__ == '__main__':
    print("Run from the main notebook pipeline.")
