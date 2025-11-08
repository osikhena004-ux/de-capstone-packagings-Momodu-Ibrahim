import json, os

from omnicart_pipeline.api_client import Client
from omnicart_pipeline.config import Configuration
from data_analyzer import Analyzer
from data_enricher import Enricher

class Pipeline:
    def __init__(self, config_manager=None, client=None, output_path="seller_performance_report.json"):
        if config_manager is not None:
            self.config = config_manager
        else:
            self.config = Configuration.from_package()

        if client is not None:
            self.client = client
        else:
            self.client = Client(
                self.config.get_base_url(),
                self.config.get_page_limit()
            )

        self.output_path = output_path

    def run(self):
        print("Pipeline execution started...")
        print("Fetching products...")
        products = self.client.get_products()
        print("Fetching users...")
        users = self.client.get_users()
        print("Enriching data...")
        df = Enricher(products, users).enrich()
        print("Generating analysis...")
        report = Analyzer(df).analyze()
        # atomic write
        tmp = self.output_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        os.replace(tmp, self.output_path)
        print(f"Pipeline complete. Report saved to {self.output_path}")
        return self.output_path