"""
data_loader.py
Loads and aligns KOTAK and HDFC Bank CSV data for pair trading.
"""

import pandas as pd
import numpy as np


def clean_volume(val):
    """Convert volume strings like '1.2K', '3.5M' to float."""
    if isinstance(val, str):
        val = val.replace(',', '').strip()
        if val.endswith('K'):
            return float(val[:-1]) * 1e3
        elif val.endswith('M'):
            return float(val[:-1]) * 1e6
        elif val.endswith('B'):
            return float(val[:-1]) * 1e9
        else:
            try:
                return float(val)
            except ValueError:
                return np.nan
    return val


def standardize_columns(df):
    """Standardize column names to lowercase and rename 'price' to 'close'."""
    df.columns = df.columns.str.strip().str.lower()
    rename_map = {'price': 'close', 'vol.': 'volume'}
    df = df.rename(columns=rename_map)
    return df


def load_pair_data(path_kotak='KOTAK Historical Data.csv',
                   path_hdbk='HDBK Historical Data.csv'):
    """
    Load, clean, and align KOTAK and HDFC Bank data by date.

    Returns:
        pair_data (pd.DataFrame): Merged OHLCV data for both stocks.
    """
    df_A = pd.read_csv(path_kotak)
    df_B = pd.read_csv(path_hdbk)

    # Standardize columns
    df_A = standardize_columns(df_A)
    df_B = standardize_columns(df_B)

    # Parse dates
    df_A['date'] = pd.to_datetime(df_A['date'], dayfirst=True, errors='coerce')
    df_B['date'] = pd.to_datetime(df_B['date'], dayfirst=True, errors='coerce')

    df_A = df_A.dropna(subset=['date']).set_index('date')
    df_B = df_B.dropna(subset=['date']).set_index('date')

    # Clean numeric OHLC columns
    for col in ['open', 'high', 'low', 'close']:
        if col in df_A.columns:
            df_A[col] = pd.to_numeric(df_A[col].astype(str).str.replace(',', ''), errors='coerce')
        if col in df_B.columns:
            df_B[col] = pd.to_numeric(df_B[col].astype(str).str.replace(',', ''), errors='coerce')

    # Clean volume
    if 'volume' in df_A.columns:
        df_A['volume'] = df_A['volume'].apply(clean_volume)
    if 'volume' in df_B.columns:
        df_B['volume'] = df_B['volume'].apply(clean_volume)

    # Merge on aligned dates
    pair_data = pd.DataFrame({
        'S1_close': df_A['close'],
        'S2_close': df_B['close'],
        'S1_open':  df_A['open'],
        'S2_open':  df_B['open'],
        'S1_high':  df_A['high'],
        'S2_high':  df_B['high'],
        'S1_low':   df_A['low'],
        'S2_low':   df_B['low'],
        'S1_volume': df_A['volume'],
        'S2_volume': df_B['volume'],
    }).dropna()

    print(f"Loaded KOTAK ({len(df_A)}) and HDBK ({len(df_B)}) → {len(pair_data)} aligned records.")
    return pair_data


if __name__ == '__main__':
    df = load_pair_data()
    print(df.head())
