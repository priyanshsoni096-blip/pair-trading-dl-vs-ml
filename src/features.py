"""
features.py
Adds 30 technical indicators and computes OLS-based spreads for KOTAK-HDFC pair.
"""

import pandas as pd
import numpy as np
import ta
import statsmodels.api as sm


def add_technical_indicators(pair_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add 30 technical indicators for both stocks in the pair.

    Args:
        pair_data: DataFrame with S1/S2 OHLCV columns.

    Returns:
        DataFrame with indicators added and NaN rows dropped.
    """
    # 1. Momentum Indicators
    pair_data['S1_rsi'] = ta.momentum.rsi(pair_data['S1_close'], window=14)
    pair_data['S2_rsi'] = ta.momentum.rsi(pair_data['S2_close'], window=14)
    pair_data['S1_mfi'] = ta.volume.money_flow_index(
        high=pair_data['S1_high'], low=pair_data['S1_low'],
        close=pair_data['S1_close'], volume=pair_data['S1_volume'], window=14)
    pair_data['S2_mfi'] = ta.volume.money_flow_index(
        high=pair_data['S2_high'], low=pair_data['S2_low'],
        close=pair_data['S2_close'], volume=pair_data['S2_volume'], window=14)

    # 2. Volume Indicators
    pair_data['S1_adi'] = ta.volume.acc_dist_index(
        high=pair_data['S1_high'], low=pair_data['S1_low'],
        close=pair_data['S1_close'], volume=pair_data['S1_volume'])
    pair_data['S2_adi'] = ta.volume.acc_dist_index(
        high=pair_data['S2_high'], low=pair_data['S2_low'],
        close=pair_data['S2_close'], volume=pair_data['S2_volume'])
    pair_data['S1_vpt'] = ta.volume.volume_price_trend(
        close=pair_data['S1_close'], volume=pair_data['S1_volume'])
    pair_data['S2_vpt'] = ta.volume.volume_price_trend(
        close=pair_data['S2_close'], volume=pair_data['S2_volume'])

    # 3. Volatility Indicators
    pair_data['S1_atr'] = ta.volatility.average_true_range(
        high=pair_data['S1_high'], low=pair_data['S1_low'],
        close=pair_data['S1_close'], window=14)
    pair_data['S2_atr'] = ta.volatility.average_true_range(
        high=pair_data['S2_high'], low=pair_data['S2_low'],
        close=pair_data['S2_close'], window=14)
    pair_data['S1_bb_ma'] = ta.volatility.bollinger_mavg(pair_data['S1_close'], window=20)
    pair_data['S2_bb_ma'] = ta.volatility.bollinger_mavg(pair_data['S2_close'], window=20)

    # 4. Trend Indicators
    pair_data['S1_adx'] = ta.trend.adx(
        high=pair_data['S1_high'], low=pair_data['S1_low'],
        close=pair_data['S1_close'], window=14)
    pair_data['S2_adx'] = ta.trend.adx(
        high=pair_data['S2_high'], low=pair_data['S2_low'],
        close=pair_data['S2_close'], window=14)
    pair_data['S1_ema'] = ta.trend.ema_indicator(pair_data['S1_close'], window=14)
    pair_data['S2_ema'] = ta.trend.ema_indicator(pair_data['S2_close'], window=14)
    pair_data['S1_macd'] = ta.trend.macd(pair_data['S1_close'], window_slow=30, window_fast=14)
    pair_data['S2_macd'] = ta.trend.macd(pair_data['S2_close'], window_slow=30, window_fast=14)

    # 5. Other Indicators
    pair_data['S1_dlr'] = ta.others.daily_log_return(pair_data['S1_close'])
    pair_data['S2_dlr'] = ta.others.daily_log_return(pair_data['S2_close'])

    pair_data = pair_data.dropna()
    print(f"Added technical indicators. Dataset shape: {pair_data.shape}")
    return pair_data


def compute_ols_spreads(pair_data: pd.DataFrame) -> pd.DataFrame:
    """
    Compute OLS-based spreads for Close, Open, High, Low prices.

    Args:
        pair_data: DataFrame with S1/S2 OHLC columns.

    Returns:
        DataFrame with Spread_Close, Spread_Open, Spread_High, Spread_Low added.
    """
    for price in ['close', 'open', 'high', 'low']:
        s1_col = f'S1_{price}'
        s2_col = f'S2_{price}'
        X = sm.add_constant(pair_data[s2_col])
        y = pair_data[s1_col]
        model = sm.OLS(y, X).fit()
        alpha = model.params['const']
        beta = model.params[s2_col]
        spread_col = f'Spread_{price.capitalize()}'
        pair_data[spread_col] = y - (beta * pair_data[s2_col] + alpha)
        print(f"{price.capitalize()} → α={alpha:.4f}, β={beta:.4f}")

    return pair_data


if __name__ == '__main__':
    from data_loader import load_pair_data
    df = load_pair_data()
    df = add_technical_indicators(df)
    df = compute_ols_spreads(df)
    print(df[['Spread_Close', 'Spread_Open', 'Spread_High', 'Spread_Low']].head())
