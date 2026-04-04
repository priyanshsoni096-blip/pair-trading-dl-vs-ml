"""
backtesting.py
Signal generation and PnL computation for pair trading strategy.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def generate_signals(spread_pred, entry_z=1.0, exit_z=0.2):
    """
    Generate trading signals based on Z-score of predicted spread.

    Args:
        spread_pred: Array of predicted spread values.
        entry_z: Z-score threshold to enter a trade.
        exit_z: Z-score threshold to exit a trade.

    Returns:
        signals (np.array): +1 (long), -1 (short), 0 (hold)
        z (np.array): Z-score series
    """
    z = (spread_pred - np.mean(spread_pred)) / np.std(spread_pred)
    signals = np.zeros_like(z)

    # Long spread: spread expected to rise
    signals[z < -entry_z] = 1
    # Short spread: spread expected to fall
    signals[z > entry_z] = -1

    # Hold position until exit signal
    for i in range(1, len(z)):
        if abs(z[i]) < exit_z:
            signals[i] = 0
        elif signals[i] == 0:
            signals[i] = signals[i - 1]

    return signals, z


def compute_returns(spread_actual, signals):
    """
    Compute daily and cumulative PnL given signals and actual spread.

    Args:
        spread_actual: Array of actual spread values.
        signals: Array of trading signals.

    Returns:
        returns (np.array): Daily returns
        cum_returns (np.array): Cumulative PnL
    """
    spread_diff = np.diff(spread_actual)
    signals = signals[:-1]
    returns = signals * spread_diff
    cum_returns = np.cumsum(returns)
    return returns, cum_returns


def run_backtest(predictions_dict, actual_spread, entry_z=0.8, exit_z=0.1):
    """
    Run full backtest for all models and print summary.

    Args:
        predictions_dict: Dict of {model_name: predictions_array}
        actual_spread: Ground truth spread array
        entry_z: Entry threshold
        exit_z: Exit threshold

    Returns:
        results_df (pd.DataFrame): Summary of RMSE, R², Sharpe, Total Return
    """
    backtest_results = {}
    summary = {}

    for model_name, preds in predictions_dict.items():
        signals, z = generate_signals(preds, entry_z=entry_z, exit_z=exit_z)
        returns, cum_returns = compute_returns(actual_spread, signals)

        sharpe = np.mean(returns) / (np.std(returns) + 1e-9)
        total_return = cum_returns[-1]

        backtest_results[model_name] = {
            'signals': signals,
            'returns': returns,
            'cum_returns': cum_returns
        }
        summary[model_name] = {
            'Sharpe': round(sharpe, 3),
            'Total Return': round(total_return, 4)
        }

    # Plot cumulative returns
    plt.figure(figsize=(15, 7))
    for model_name, data in backtest_results.items():
        plt.plot(data['cum_returns'],
                 label=f"{model_name} (Sharpe={summary[model_name]['Sharpe']}, "
                       f"PnL={summary[model_name]['Total Return']})",
                 linewidth=2)

    plt.title("Cumulative Returns — Pair Trading Simulation")
    plt.xlabel("Time Step (Trade Day)")
    plt.ylabel("Cumulative PnL (Z-Score points)")
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linestyle='--')
    plt.tight_layout()
    plt.savefig('cumulative_pnl.png')
    plt.show()

    results_df = pd.DataFrame(summary).T
    print("\nFINAL BACKTEST SUMMARY")
    print(results_df.sort_values('Sharpe', ascending=False))
    return results_df


if __name__ == '__main__':
    print("Run from the main notebook pipeline.")
