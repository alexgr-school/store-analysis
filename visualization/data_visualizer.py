import os

import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()
graphics_folder_path = os.getenv("GRAPHICS_FOLDER_PATH") or "./output/graphics"


class DataVisualizer:
    def __init__(self, data):
        self.data = data

    def plot_price_dispersion(self, view=False):
        plt.figure(figsize=(10, 6))
        sns.boxplot(
            x="categ",
            y="price",
            data=self.data,
            palette={"0.0": "#14617B", "1.0": "#9E1E64", "2.0": "#FF8902"},
        )
        plt.title("Dispersion des prix par catégorie de produits")
        plt.xlabel("Catégorie")
        plt.ylabel("Prix")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "price_dispersion.png")
        plt.savefig(file_path, dpi=300)
        if view:
            plt.show()

    def plot_sales_over_time(self, view=False):
        self.data["month"] = self.data["date"].dt.to_period("M")
        sales_per_month = self.data.groupby("month").size()
        plt.figure(figsize=(12, 6))
        sales_per_month.plot(kind="line", marker="o")
        plt.title("Nombre de ventes par mois")
        plt.xlabel("Mois")
        plt.ylabel("Nombre de ventes")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "sales_over_time.png")
        plt.savefig(file_path, dpi=300)
        if view:
            plt.show()

    def plot_sales_per_age(self, view=False):
        plt.figure(figsize=(12, 6))
        sns.histplot(self.data["age"], bins=20)
        plt.title("Répartition des ventes par âge")
        plt.xlabel("Âge")
        plt.ylabel("Nombre de ventes")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "sales_per_age.png")
        plt.savefig(file_path, dpi=300)
        if view:
            plt.show()

    def plot_sales_per_age_category(self, view=False):
        plt.figure(figsize=(12, 6))
        sns.histplot(self.data, x="age", hue="categ", bins=20, multiple="stack")
        plt.title("Répartition des ventes par âge et par catégorie")
        plt.xlabel("Âge")
        plt.ylabel("Nombre de ventes")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "sales_per_age_category.png")
        plt.savefig(file_path, dpi=300)
        if view:
            plt.show()

    def plot_sales_per_sex_age(self, view=False):
        self.data["sex"] = self.data["sex"].map({"m": "Homme", "f": "Femme"})

        plt.figure(figsize=(12, 6))
        sns.boxplot(
            x="sex",
            y="age",
            data=self.data,
            order=["Homme", "Femme"],
            palette={"Homme": "#14617B", "Femme": "#FFB560"},
        )
        plt.title("Sexe par Âge")
        plt.xlabel("Sexe")
        plt.ylabel("Âge")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "sales_per_sex_age.png")
        plt.savefig(file_path, dpi=300)
        if view:
            plt.show()

    def plot_average_purchase(self, view=False):
        # Calcul du montant total des achats par client
        metrics_df = (
            self.data.groupby("client_id")
            .agg(
                {
                    "price": "sum",
                    "session_id": "nunique",
                    "categ": lambda x: x.mode().iloc[0],
                }
            )
            .rename(
                columns={
                    "price": "Total Purchase",
                    "session_id": "Frequency",
                    "categ": "Most Purchased Category",
                }
            )
            .reset_index()
        )

        sns.histplot(
            metrics_df["Total Purchase"] / metrics_df["Frequency"],
            bins=30,
            kde=False,
            color="#0BBB9E",
        )
        plt.title("Distribution de la Taille Moyenne du Panier")
        plt.xlabel("Taille Moyenne du Panier")
        plt.ylabel("Nombre de Clients")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "average_purchase.png")
        plt.savefig(file_path, dpi=300)
        if view:
            plt.show()
