import pandas as pd
from omnicart_pipeline.data_analyzer import Analyzer

def test_per_seller_stats():
    df = pd.DataFrame([
        {"username": "alice", "price": 10, "revenue": 20},
        {"username": "alice", "price": 20, "revenue": 40},
        {"username": "bob", "price": 30, "revenue": 30},
    ])
    analyzer = Analyzer(df)
    stats = analyzer.per_seller_stats()
    assert "alice" in stats and "bob" in stats
    assert stats["alice"]["total_revenue"] == 60
    assert stats["alice"]["num_products"] == 2
