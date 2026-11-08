"""CLI for episodic-consolidation-worker."""
import sys
import argparse
from .worker import EpisodicConsolidationWorker


def main():
    parser = argparse.ArgumentParser(description="Episodic Consolidation Worker CLI")
    parser.add_argument("--demo", action="store_true", help="Run episodic experience consolidation demo")
    args = parser.parse_args()

    if args.demo:
        worker = EpisodicConsolidationWorker(min_support=2, min_confidence=0.7)
        worker.record_experience("EADDRINUSE", "kill_port_process", True)
        worker.record_experience("EADDRINUSE", "kill_port_process", True)
        worker.record_experience("EADDRINUSE", "ignore_and_retry", False)

        schemas = worker.consolidate()
        print(f"[+] Consolidated {len(schemas)} declarative schemas from episodic buffer:")
        for s in schemas:
            print(f"    Trigger: {s.trigger} -> Recommended Action: {s.recommended_action} (Confidence: {s.confidence*100:.1f}%)")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
