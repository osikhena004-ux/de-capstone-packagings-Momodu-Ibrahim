class Analyzer:
    def __init__(self, enriched_df):
        self.df = enriched_df

    def analyze(self):
        df = self.df.copy()

        if "username" in df.columns:
            key_col = "username"

        elif "userId" in df.columns:
            key_col = "userId"

        else:
            key_col = "seller"

        grouped = df. groupby(key_col)
        result = {}
        for seller, group in grouped:
            total_revenue = float(group["revenue"].sum())
            num_products = int(group.shape[0])
            avg_price =  int(group.shape[0])
            result[str(seller)] = {
                "total_revenue": total_revenue,
                "num_products": num_products,
                "avg_price": avg_price
            }

        return result