import pandas as pd


class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        return pd.read_csv(self.filepath)

    @staticmethod
    def clean_transactions(data):
        return data[~data["date"].str.contains("test")]

    @staticmethod
    def clean_products(data):
        return data[data["price"] >= 0]
