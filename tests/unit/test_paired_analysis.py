import pytest

from capc_sim.analysis.paired import jain_completion_ratio, starvation_threshold


def test_starvation_threshold_equation_3_9():
    assert starvation_threshold([0.01, 0.02, 0.03]) == 0.50
    assert starvation_threshold([0.20, 0.30, 0.40]) == pytest.approx(1.50)


def test_jain_completion_ratio_perfect_when_equal():
    completed = {"HIGH": 9, "MEDIUM": 18, "LOW": 27}
    admitted = {"HIGH": 10, "MEDIUM": 20, "LOW": 30}
    assert jain_completion_ratio(completed, admitted) == pytest.approx(1.0)
