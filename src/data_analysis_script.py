import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Chargement des données
transactions = pd.read_csv("./data/transactions.csv")
customers = pd.read_csv("./data/customers.csv")
products = pd.read_csv("./data/products.csv")

# Nettoyage des données
## Suppression des entrées de test dans les transactions
transactions = transactions[~transactions["date"].str.contains("test")]

## Suppression du produit avec un prix négatif
products = products[products["price"] >= 0]

# Fusion des données
transactions = pd.merge(transactions, customers, on="client_id", how="left")
complete_data = pd.merge(transactions, products, on="id_prod", how="left")

# Conversion de la colonne 'date' en datetime
complete_data["date"] = pd.to_datetime(complete_data["date"])

# Exploration des données
## Dispersion des prix par catégorie
plt.figure(figsize=(10, 6))
sns.boxplot(x="categ", y="price", data=complete_data)
plt.title("Dispersion des prix par catégorie de produits")
plt.xlabel("Catégorie")
plt.ylabel("Prix")
plt.grid(True)
plt.show()

## Évolution des ventes au fil du temps
complete_data["month"] = complete_data["date"].dt.to_period("M")
sales_per_month = complete_data.groupby("month").size()
plt.figure(figsize=(12, 6))
sales_per_month.plot(kind="line", marker="o")
plt.title("Nombre de ventes par mois")
plt.xlabel("Mois")
plt.ylabel("Nombre de ventes")
plt.grid(True)
plt.show()

# afficher les rep

# Calcul de l'âge des clients
complete_data["age"] = 2024 - complete_data["birth"]


# Sauvegarde du jeu de données nettoyé et fusionné
complete_data.to_csv("./data/generated/cleaned_complete_data.csv", index=False)
