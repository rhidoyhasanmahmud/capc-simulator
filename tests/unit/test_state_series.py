import pandas as pd
import pytest

from capc_sim.analysis.state_series import continuous_time_linear_slope, time_weighted_mean


def test_time_weighted_mean_piecewise_state():
    df = pd.DataFrame([
        {"time": 0.0, "queue_length": 0},
        {"time": 2.0, "queue_length": 2},
        {"time": 4.0, "queue_length": 0},
    ])
    assert time_weighted_mean(df, "queue_length", 0.0, 6.0) == pytest.approx(4.0 / 6.0)


def test_continuous_time_slope_zero_for_constant_state():
    df = pd.DataFrame([
        {"time": 0.0, "queue_length": 3},
        {"time": 10.0, "queue_length": 3},
    ])
    assert continuous_time_linear_slope(df, "queue_length", 0.0, 10.0) == pytest.approx(0.0)
