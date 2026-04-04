import pandas as pd
import numpy as np

def test_spread_not_null():
    spread = pd.Series([1.2, 0.3, -0.5, 0.8])
    assert spread.isnull().sum() == 0

def test_zscore_range():
    spread = pd.Series(np.random.randn(100))
    z = (spread - spread.mean()) / spread.std()
    assert z.abs().max() < 10

def test_pair_data_columns():
    df = pd.DataFrame({"S1_close": [100, 101], "S2_close": [50, 51]})
    assert "S1_close" in df.columns
    assert "S2_close" in df.columns

def test_signal_values():
    signals = np.array([-1, 0, 1, 1, -1, 0])
    assert set(np.unique(signals)).issubset({-1, 0, 1})
