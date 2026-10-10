# Output Schema

Each run has its own directory named from shard count, cross-shard ratio, worker count, scheduler, and seed.

## `transactions.csv`
Minimum fields include:

- `run_id`, `seed`, `scheduler`, `shard_count`, `cross_shard_ratio`, `workers`, `transaction_id`
- `arrival_time`, `queue_entry_time`, `service_start_time`, `completion_time`
- `waiting_time`, `service_time`, `latency`
- `priority`, `workload_state`
- `required_shards`, `dependency_degree`, `is_cross_shard`
- `status`, `completed_by_cutoff`
- `arrival_rate_at_entry`
- `queue_length_at_entry`
- `active_lock_conflicts_at_entry`

The queue-entry fields are the primary RQ2 predictors and are recorded before subsequent waiting time is realized.

## `decisions.csv`
One row per dispatched cross-shard transaction.

Common fields:
- selection time;
- transaction identity;
- priority and shard set;
- waiting age;
- candidate/eligible/blocked counts;
- selection rule.

CAPC rows additionally contain:
- CAPC score;
- contention score and label;
- normalized contention components;
- urgency;
- aging;
- dependency burden;
- recent lock pressure.

## `dispatch_snapshots.csv`
Records queue/eligibility state at scheduling opportunities. It supports implementation diagnostics and the neutral-pilot lock-block diagnostic.

The repository operationalizes the pilot lock-block fraction as:

```text
sum(blocked candidate observations) / sum(all queued candidate observations)
```

This is an explicit implementation convention and should be kept fixed once the final pilot protocol is approved.

## `state_events.csv`
Timestamped post-event state:
- queue length;
- active workers;
- locked shard count;
- workload state.

Time-weighted queue and worker statistics are reconstructed from these state-change intervals.

## `summary.json`
Run-level metrics including:
- mean/median/p95/p99 cross-shard latency;
- mean/p95/max waiting;
- mean service time;
- coordination throughput;
- mean/max queue;
- p95-minus-median latency spread;
- worker utilization;
- class completion ratios;
- Jain completion-ratio index;
- unfinished fraction at cutoff;
- final queue slope;
- lock-block diagnostics;
- post-burst recovery summary;
- queue stability status;
- RQ2 run-level predictor summaries.

## `queue_recovery.json`
Contains the evaluability, threshold, recovery status, and recovery delay for each burst episode considered by the Chapter 3 stability rule.

## `metadata.json`
Contains:
- config hash;
- trace hash;
- Git commit if available;
- Python version;
- OS/platform/processor string;
- relevant package versions;
- cutoff snapshot;
- schema version.

## `effective_config.yaml`
The exact configuration object used by the run.

## Matrix-level files

- `matrix_summary.csv`
- `pair_integrity.csv`
- `matrix_manifest.json`
- `failures.json`

These files allow a final thesis result to be traced from a table/figure back to the exact run set and configuration.
