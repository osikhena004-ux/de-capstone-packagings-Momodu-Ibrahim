from __future__ import annotations
import argparse
from .config import Configuration
from .pipeline import Pipeline


def main(argv=None):
    parser = argparse.ArgumentParser(prog="omnicart-pipeline",
                                     description = "Run the OmniCart data enrichment pipeline.")
    parser.add_argument("--output", "-o",
                        default = "seller_performance_report.json", help="Output report path")
    args = parser.parse_args(argv)

    config = Configuration.from_package()
    pipeline = Pipeline(config_manager=config, output_path=args.output)
    pipeline.run()


if __name__ == "__main__":
    main()
