from omnicart_pipeline.data_enricher import Enricher

def test_enricher_computes_revenue():
    products = [
        {"id": 1, "price": 10, "rating": {"count": 2, "userId": 1}},
        {"id": 2, "price": 5, "rating": {"count": 4, "userId": 1}},
    ]
    users = [{"id": 1, "username": "seller1"}]

    enricher = Enricher(products, users)
    df = enricher.to_enriched_dataframe()

    assert "revenue" in df.columns
    assert df["revenue"].sum() == 10 * 2 + 5 * 4


def test_merge_with_missing_user():
    products = [{"id": 1, "price": 10, "rating": {"count": 1}}]
    users = []

    enricher = Enricher(products, users)
    df = enricher.to_enriched_dataframe()

    assert "revenue" in df.columns

