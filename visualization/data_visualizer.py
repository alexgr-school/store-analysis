import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from dotenv import load_dotenv

load_dotenv()
graphics_folder_path = os.getenv("GRAPHICS_FOLDER_PATH") or "./output/graphics"


class DataVisualizer:
    def __init__(self, data, view=False):
        self.data = data
        self.view = view

    def plot_price_dispersion(self):
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
        if self.view:
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
        file_path = os.path.join(graphics_folder_path, "sales_over_time.png")
        plt.savefig(file_path, dpi=300)
        if self.view:
            plt.show()

    def plot_sales_per_age(self):
        plt.figure(figsize=(12, 6))
        sns.histplot(self.data["age"], bins=20)
        plt.title("Répartition des ventes par âge")
        plt.xlabel("Âge")
        plt.ylabel("Nombre de ventes")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "sales_per_age.png")
        plt.savefig(file_path, dpi=300)
        if self.view:
            plt.show()

    def plot_sales_per_age_category(self):
        plt.figure(figsize=(12, 6))
        sns.histplot(self.data, x="age", hue="categ", bins=20, multiple="stack")
        plt.title("Répartition des ventes par âge et par catégorie")
        plt.xlabel("Âge")
        plt.ylabel("Nombre de ventes")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "sales_per_age_category.png")
        plt.savefig(file_path, dpi=300)
        if self.view:
            plt.show()

    def plot_sales_per_sex_age(self):
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
        if self.view:
            plt.show()

    def plot_transaction_price_average(self):
        # Calcul du montant total des achats par client
        metrics_df = (
            self.data.groupby("price")
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
        plt.title("Montant moyen des achats par transaction")
        plt.xlabel("Nombre de transactions")
        plt.ylabel("Prix moyen")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "transaction_price_average.png")
        plt.savefig(file_path, dpi=300)
        if self.view:
            plt.show()

    def plot_age_dispersal(self):
        tmp_data = self.data.drop_duplicates(subset="client_id")

        plt.figure(figsize=(12, 6))
        sns.histplot(tmp_data["age"], bins=20)
        plt.title("Répartition des âges")
        plt.xlabel("Âge")
        plt.ylabel("Nombre de clients")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "age_dispersal.png")
        plt.savefig(file_path, dpi=300)
        if self.view:
            plt.show()

    def plot_products_price_lorenz_curve(self):
        # Supprimer les doublons basés sur 'id_prod'
        df = self.data.drop_duplicates(subset=["id_prod"])
        df = df.dropna(subset=["price"])

        # Trier les valeurs par prix pour la courbe de Lorenz
        df_sorted = df.sort_values(by="price")

        # Calculer la part cumulée des prix et la part cumulée des produits
        cumulative_price = df_sorted["price"].cumsum() / df_sorted["price"].sum()
        cumulative_price = np.insert(
            cumulative_price.values, 0, 0
        )  # Ajouter 0 au début pour la courbe
        cumulative_products = np.linspace(0, 1, len(cumulative_price))

        # Calculer l'indice de Gini
        area_under_lorenz_curve = np.trapz(
            cumulative_price, dx=1 / len(cumulative_products)
        )
        gini_index = 1 - 2 * area_under_lorenz_curve

        # Création de la courbe de Lorenz
        plt.figure(figsize=(10, 6))
        plt.plot(
            cumulative_products,
            cumulative_price,
            label="Courbe de Lorenz",
            color="blue",
        )
        plt.fill_between(cumulative_products, cumulative_price, alpha=0.2, color="blue")
        plt.plot(
            [0, 1],
            [0, 1],
            label="Ligne d'égalité parfaite",
            linestyle="--",
            color="red",
        )

        # Ajout de détails au graphique
        plt.title(
            f"Courbe de Lorenz pour les prix des produits\nIndice de Gini: {gini_index:.2f}"
        )
        plt.xlabel("Part cumulée des produits")
        plt.ylabel("Part cumulée des prix")
        plt.legend()

        file_path = os.path.join(
            graphics_folder_path, "products_price_lorenz_curve.png"
        )
        plt.savefig(file_path, dpi=300)
        if self.view:
            plt.show()

    def plot_clients_age_lorenz_curve(self):
        # Supprimer les doublons basés sur 'id_prod'
        df = self.data.drop_duplicates(subset=["client_id"])
        df = df.dropna(subset=["age"])

        # Trier les valeurs par prix pour la courbe de Lorenz
        df_sorted = df.sort_values(by="age")

        # Calculer la part cumulée des prix et la part cumulée des produits
        cumulative_age = df_sorted["age"].cumsum() / df_sorted["age"].sum()
        cumulative_age = np.insert(
            cumulative_age.values, 0, 0
        )  # Ajouter 0 au début pour la courbe
        cumulative_clients = np.linspace(0, 1, len(cumulative_age))

        # Calculer l'indice de Gini
        area_under_lorenz_curve = np.trapz(
            cumulative_age, dx=1 / len(cumulative_clients)
        )
        gini_index = 1 - 2 * area_under_lorenz_curve

        # Création de la courbe de Lorenz
        plt.figure(figsize=(10, 6))
        plt.plot(
            cumulative_clients,
            cumulative_age,
            label="Courbe de Lorenz",
            color="blue",
        )
        plt.fill_between(cumulative_clients, cumulative_age, alpha=0.2, color="blue")
        plt.plot(
            [0, 1],
            [0, 1],
            label="Ligne d'égalité parfaite",
            linestyle="--",
            color="red",
        )

        # Ajout de détails au graphique
        plt.title(
            f"Courbe de Lorenz pour les âges des clients\nIndice de Gini: {gini_index:.2f}"
        )
        plt.xlabel("Part cumulée des clients")
        plt.ylabel("Part cumulée des âges")
        plt.legend()

        file_path = os.path.join(graphics_folder_path, "clients_age_lorenz_curve.png")
        plt.savefig(file_path, dpi=300)
        if self.view:
            plt.show()

    def plot_expenses_per_age(self):
        # Calculer la somme des dépenses pour chaque âge
        expenses_per_age = self.data.groupby("age")["price"].sum().reset_index()

        # Créer le graphique à bulles
        plt.figure(figsize=(12, 6))
        plt.scatter(
            expenses_per_age["age"],
            expenses_per_age["price"],
            s=expenses_per_age["price"] / expenses_per_age["price"].max() * 1000,
            alpha=0.5,
        )
        plt.title("Dépenses Totales par Âge")
        plt.xlabel("Âge")
        plt.ylabel("Dépenses Totales")
        plt.grid(True)
        file_path = os.path.join(graphics_folder_path, "expenses_per_age.png")
        plt.savefig(file_path, dpi=300)
        if self.view:
            plt.show()
