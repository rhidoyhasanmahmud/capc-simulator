from dataclasses import replace

import pandas as pd

from capc_sim.model.enums import PriorityClass, WorkloadState
from capc_sim.model.transaction import TransactionSpec
from capc_sim.simulation.engine import Simulator
from capc_sim.workload.trace import StateInterval, Trace


def small_trace():
    return Trace(
        transactions=(
            TransactionSpec(1, 0.10, (0,1), PriorityClass.MEDIUM, WorkloadState.NORMAL, 0.50, True),
            TransactionSpec(2, 0.10, (0,2), PriorityClass.HIGH, WorkloadState.NORMAL, 0.10, True),
            TransactionSpec(3, 0.10, (2,3), PriorityClass.LOW, WorkloadState.NORMAL, 0.10, True),
        ),
        state_intervals=(StateInterval(WorkloadState.NORMAL, 0.0, 2.0),),
    )


def short_config(dev_config):
    return replace(
        dev_config,
        simulation=replace(dev_config.simulation, duration_s=2.0, warmup_s=0.0),
        coordination=replace(dev_config.coordination, workers=2),
    )


def test_atomic_scheduler_never_overlaps_conflicting_shards(tmp_path, dev_config):
    cfg = short_config(dev_config)
    result = Simulator(cfg, small_trace(), "static_atomic_fifo", 1).run(tmp_path)
    tx = pd.read_csv(result.output_dir / "transactions.csv").set_index("transaction_id")
    assert tx.loc[2, "service_start_time"] >= tx.loc[1, "completion_time"]


def test_multi_worker_dispatches_non_conflicting_transactions(tmp_path, dev_config):
    cfg = short_config(dev_config)
    result = Simulator(cfg, small_trace(), "static_atomic_fifo", 1).run(tmp_path)
    tx = pd.read_csv(result.output_dir / "transactions.csv").set_index("transaction_id")
    assert tx.loc[1, "service_start_time"] == tx.loc[3, "service_start_time"]


def test_diagnostic_fifo_is_non_atomic_reference(tmp_path, dev_config):
    cfg = short_config(dev_config)
    result = Simulator(cfg, small_trace(), "diagnostic_fifo", 1).run(tmp_path)
    tx = pd.read_csv(result.output_dir / "transactions.csv").set_index("transaction_id")
    assert tx.loc[1, "service_start_time"] == tx.loc[2, "service_start_time"]


def test_run_writes_required_provenance_outputs(tmp_path, dev_config):
    cfg = short_config(dev_config)
    result = Simulator(cfg, small_trace(), "capc", 1).run(tmp_path)
    required = {
        "trace.csv", "workload_states.csv", "transactions.csv", "decisions.csv",
        "dispatch_snapshots.csv", "state_events.csv", "summary.json", "metadata.json",
        "queue_recovery.json", "effective_config.yaml",
    }
    assert required.issubset({p.name for p in result.output_dir.iterdir()})


def test_transaction_output_carries_condition_columns(tmp_path, dev_config):
    cfg = short_config(dev_config)
    result = Simulator(cfg, small_trace(), "static_atomic_fifo", 1).run(tmp_path)
    tx = pd.read_csv(result.output_dir / "transactions.csv")
    assert {"shard_count", "cross_shard_ratio", "workers"}.issubset(tx.columns)
    assert set(tx["shard_count"]) == {cfg.sharding.shard_count}
    assert set(tx["workers"]) == {cfg.coordination.workers}

