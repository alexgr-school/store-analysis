import matplotlib.pyplot as plt
import seaborn as sns


class DataVisualizer:
    def __init__(self, data):
        self.data = data

    def plot_price_dispersion(self):
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="categ", y="price", data=self.data)
        plt.title("Dispersion des prix par catégorie de produits")
        plt.xlabel("Catégorie")
        plt.ylabel("Prix")
        plt.grid(True)
        plt.show()

    def plot_sales_over_time(self):
        self.data["month"] = self.data["date"].dt.to_period("M")
        sales_per_month = self.data.groupby("month").size()
        plt.figure(figsize=(12, 6))
        sales_per_month.plot(kind="line", marker="o")
        plt.title("Nombre de ventes par mois")
        plt.xlabel("Mois")
        plt.ylabel("Nombre de ventes")
        plt.grid(True)
        plt.show()
