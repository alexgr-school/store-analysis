import pandas as pd


class DataAnalyzer:
    def __init__(self, transactions, customers, products):
        self.transactions = transactions
        self.customers = customers
        self.products = products

    def merge_data(self):
        transactions_customers = pd.merge(
            self.transactions, self.customers, on="client_id", how="left"
        )
        complete_data = pd.merge(
            transactions_customers, self.products, on="id_prod", how="left"
        )
        complete_data["date"] = pd.to_datetime(complete_data["date"])
        complete_data["age"] = 2024 - complete_data["birth"]
        return complete_data
