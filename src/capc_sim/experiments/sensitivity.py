from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from capc_sim.config.schema import ExperimentConfig


WORKLOAD_BURST_LEVELS = (40.0, 60.0, 80.0)
Q_BN_LEVELS = (0.05, 0.10, 0.20)
DEPENDENCY_TWO_SHARD_LEVELS = (1.0, 0.8, 0.5)  # maps to 100/0, 80/20, 50/50
SERVICE_MULTIPLIERS = (0.8, 1.0, 1.2)
WEIGHT_MULTIPLIERS = (0.5, 1.0, 1.5)
THRESHOLD_MULTIPLIERS = (0.8, 1.0, 1.2)


def workload_sensitivity_configs(base: ExperimentConfig) -> Iterable[tuple[str, ExperimentConfig]]:
    for burst in WORKLOAD_BURST_LEVELS:
        yield f"lambdaB_{burst:g}", replace(base, workload=replace(base.workload, lambda_burst=burst))
    for qbn in Q_BN_LEVELS:
        yield f"qBN_{qbn:g}", replace(base, workload=replace(base.workload, q_burst_to_normal=qbn))
    for p2 in DEPENDENCY_TWO_SHARD_LEVELS:
        yield f"dependency_{int(round(100*p2))}_{int(round(100*(1-p2)))}", replace(
            base, sharding=replace(base.sharding, two_shard_probability=p2)
        )
    for m in SERVICE_MULTIPLIERS:
        service = base.coordination.service_time_ms
        yield f"service_x{m:g}", replace(
            base,
            coordination=replace(
                base.coordination,
                service_time_ms=replace(service, min=service.min * m, max=service.max * m),
            ),
        )


def capc_one_at_a_time_configs(base: ExperimentConfig) -> Iterable[tuple[str, ExperimentConfig]]:
    """Generate predeclared one-at-a-time weight/threshold perturbations.

    The base config must already contain frozen CAPC parameters. Contention weights
    are re-normalized after varying one component so that the convex-sum constraint
    remains satisfied; this implementation convention is documented and should be
    confirmed before final sensitivity execution.
    """
    if base.capc.missing_fields():
        raise ValueError("CAPC sensitivity requires a fully frozen base configuration")

    rw = base.capc.ranking_weights
    for field in ("urgency", "aging", "dependency", "lock_pressure"):
        original = float(getattr(rw, field))
        for m in WEIGHT_MULTIPLIERS:
            new_rw = replace(rw, **{field: original * m})
            yield f"ranking_{field}_x{m:g}", replace(base, capc=replace(base.capc, ranking_weights=new_rw))

    cw = base.capc.contention_weights
    fields = ("arrival", "queue", "dependency", "lock")
    for field in fields:
        original = float(getattr(cw, field))
        for m in WEIGHT_MULTIPLIERS:
            raw = {name: float(getattr(cw, name)) for name in fields}
            raw[field] = original * m
            total = sum(raw.values())
            normalized = {name: value / total for name, value in raw.items()}
            new_cw = replace(cw, **normalized)
            yield f"contention_{field}_x{m:g}", replace(base, capc=replace(base.capc, contention_weights=new_cw))

    th = base.capc.thresholds
    for field in ("low_medium", "medium_high"):
        original = float(getattr(th, field))
        for m in THRESHOLD_MULTIPLIERS:
            value = original * m
            new_th = replace(th, **{field: value})
            if new_th.low_medium is not None and new_th.medium_high is not None and 0 < new_th.low_medium < new_th.medium_high < 1:
                yield f"threshold_{field}_x{m:g}", replace(base, capc=replace(base.capc, thresholds=new_th))
