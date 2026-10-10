from capc_sim.experiments.verify import verification_passed, verification_report


def test_v1_to_v12_verification_report_passes(dev_config):
    report = verification_report(dev_config)
    assert set(report) == {f"V{i}" for i in range(1, 13)}
    assert verification_passed(report)
