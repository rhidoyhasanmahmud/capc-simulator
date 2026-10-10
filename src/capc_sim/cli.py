from __future__ import annotations

import argparse
import json
from pathlib import Path

from capc_sim.config.loader import load_config
from capc_sim.experiments.pilot import run_neutral_pilot
from capc_sim.experiments.runner import run_matrix, run_single
from capc_sim.experiments.verify import verification_passed, verification_report


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="capc-sim", description="CAPC research simulator")
    sub = p.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run one scheduler/seed")
    run.add_argument("--config", required=True)
    run.add_argument("--scheduler", required=True)
    run.add_argument("--seed", required=True, type=int)
    run.add_argument("--output", default="results")

    matrix = sub.add_parser("matrix", help="Run a paired experiment matrix")
    matrix.add_argument("--config", required=True)
    matrix.add_argument("--seeds", nargs="+", type=int, required=True)
    matrix.add_argument("--shards", nargs="+", type=int)
    matrix.add_argument("--ratios", nargs="+", type=float)
    matrix.add_argument("--workers", nargs="+", type=int)
    matrix.add_argument("--schedulers", nargs="+")
    matrix.add_argument("--output", default="results/matrix")
    matrix.add_argument("--continue-on-error", action="store_true")

    pilot = sub.add_parser("pilot", help="Run Static Atomic FIFO neutral-pilot matrix only")
    pilot.add_argument("--config", required=True)
    pilot.add_argument("--seeds", nargs="+", type=int, required=True)
    pilot.add_argument("--shards", nargs="+", type=int)
    pilot.add_argument("--ratios", nargs="+", type=float)
    pilot.add_argument("--workers", nargs="+", type=int)
    pilot.add_argument("--output", default="results/pilot")

    verify = sub.add_parser("verify", help="Run the Chapter 5 V1-V12 deterministic verification checks")
    verify.add_argument("--config", required=True)
    verify.add_argument("--json-output")
    return p


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    config = load_config(args.config)

    if args.command == "run":
        result = run_single(config, args.scheduler, args.seed, args.output)
        print(json.dumps({
            "run_id": result.run_id,
            "output_dir": str(result.output_dir),
            "trace_hash": result.trace_hash,
            "summary": result.summary,
        }, indent=2))
        return 0

    if args.command == "matrix":
        df = run_matrix(
            config,
            seeds=args.seeds,
            output=args.output,
            shard_counts=args.shards,
            cross_shard_ratios=args.ratios,
            workers=args.workers,
            schedulers=args.schedulers,
            fail_fast=not args.continue_on_error,
        )
        print(f"Completed {len(df)} runs. Summary: {Path(args.output) / 'matrix_summary.csv'}")
        return 0

    if args.command == "pilot":
        df = run_neutral_pilot(
            config,
            seeds=args.seeds,
            output=args.output,
            shard_counts=args.shards,
            cross_shard_ratios=args.ratios,
            workers=args.workers,
        )
        print(f"Completed {len(df)} Static Atomic FIFO pilot runs. Summary: {Path(args.output) / 'matrix_summary.csv'}")
        return 0

    if args.command == "verify":
        report = verification_report(config)
        payload = {
            "passed": verification_passed(report),
            "checks": report,
        }
        text = json.dumps(payload, indent=2)
        print(text)
        if args.json_output:
            path = Path(args.json_output)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text + "\n", encoding="utf-8")
        return 0 if payload["passed"] else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
