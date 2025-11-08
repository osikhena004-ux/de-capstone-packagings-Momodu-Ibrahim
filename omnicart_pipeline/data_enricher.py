import pandas as pd
class Enricher:
    def __init__(self, products, users):
        self.products = products
        self.users = users

    def enrich(self):
        products_df = pd.json_normalize(self.products)
        users_df = pd.json_normalize(self.users)

        enriched = products_df.merge(users_df, left_on = "useId", right_on = "id",
                                     how = "left", suffixes = ("", "_user"))

        if "rating.count" in enriched.columns:
            rating_count = pd.to_numeric(enriched["rating.count"],
                                         errors = "coerce").fillna(0).astype(int)

        elif "rating" in enriched.columns:
            rating_count = enriched["rating"].apply(lambda r: r.get("count", 0)
            if isinstance(r, dict) else 0)

        else:
            rating_count = pd.Series(0, index = enriched.index)

        enriched["rating_count"] = rating_count
        enriched["price"] = pd.to_numeric(enriched.get("price", 0),
                                          errors = "coerce").fillna(0)
        enriched["revenue"] = enriched["price"] * enriched["rating_count"]
        return enriched

