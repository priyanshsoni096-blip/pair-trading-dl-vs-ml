"""
cnn_lstm.py
CNN-LSTM hybrid model for Z-Score spread prediction.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import (Conv1D, MaxPooling1D, BatchNormalization,
                                         LSTM, Dropout, Dense)
    from tensorflow.keras.regularizers import l2
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
except ImportError:
    print("TensorFlow not installed. CNN-LSTM model unavailable.")


def build_cnn_lstm(input_shape):
    """
    Build and compile the CNN-LSTM hybrid model.

    Args:
        input_shape: Tuple (lookback, n_features).

    Returns:
        Compiled Keras Sequential model.
    """
    model = Sequential([
        Conv1D(256, kernel_size=5, activation='relu', padding='same',
               input_shape=input_shape),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Dropout(0.1),
        LSTM(128, return_sequences=True),
        Dropout(0.1),
        LSTM(64, return_sequences=False),
        Dense(32, activation='relu', kernel_regularizer=l2(1e-4)),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    print(model.summary())
    return model


def train_cnn_lstm(model, trainX, trainY, epochs=150, batch_size=64):
    """
    Train the CNN-LSTM model with early stopping.

    Returns:
        Trained model and training history.
    """
    es = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
    lr_sched = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-5)

    history = model.fit(
        trainX, trainY,
        validation_split=0.1,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[es, lr_sched],
        verbose=1
    )
    print("CNN-LSTM training complete.")
    return model, history


def evaluate_cnn_lstm(model, testX, testY, y_scaler):
    """
    Evaluate CNN-LSTM model and return predictions + metrics.

    Returns:
        cnn_pred (np.array), metrics (dict)
    """
    pred_scaled = model.predict(testX).flatten()
    cnn_pred = y_scaler.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()
    actual = y_scaler.inverse_transform(testY.reshape(-1, 1)).flatten()

    rmse = np.sqrt(mean_squared_error(actual, cnn_pred))
    r2 = r2_score(actual, cnn_pred)

    print(f"CNN-LSTM → RMSE: {rmse:.4f} | R²: {r2:.4f}")

    plt.figure(figsize=(13, 6))
    plt.plot(actual, color='black', linewidth=2, label='Actual Z-Spread')
    plt.plot(cnn_pred, color='purple', alpha=0.8, label='CNN-LSTM Predicted')
    plt.title("CNN-LSTM — Predicted vs Actual Z-Score Spread")
    plt.xlabel("Time Step")
    plt.ylabel("Z-Score Spread")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('cnn_lstm_predictions.png')
    plt.show()

    return cnn_pred, {'RMSE': rmse, 'R²': r2}


if __name__ == '__main__':
    print("Run from the main notebook pipeline.")
