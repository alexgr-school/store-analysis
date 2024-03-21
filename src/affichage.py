import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Chargement du fichier CSV nettoyé
cleaned_data = pd.read_csv("./data/generated/cleaned_complete_data.csv")

# Calculs nécessaires pour les graphiques
## Calcul de la taille moyenne du panier et de la catégorie la plus achetée par client
metrics_df = cleaned_data.groupby('client_id').agg({
    'price': 'sum',
    'session_id': 'nunique',
    'categ': lambda x: x.mode().iloc[0]
}).rename(columns={'price': 'Total Purchase', 'session_id': 'Frequency', 'categ': 'Most Purchased Category'}).reset_index()

## Calcul du nombre de ventes par mois
cleaned_data['date'] = pd.to_datetime(cleaned_data['date'])
cleaned_data['month'] = cleaned_data['date'].dt.to_period('M')
sales_per_month = cleaned_data.groupby('month').size()

# Création des graphiques
plt.figure(figsize=(15, 10))

# Taille moyenne du panier
plt.subplot(2, 2, 1)
sns.histplot(metrics_df['Total Purchase'] / metrics_df['Frequency'], bins=30, kde=False, color='red')
plt.title('Distribution de la Taille Moyenne du Panier')
plt.xlabel('Taille Moyenne du Panier')
plt.ylabel('Nombre de Clients')

# Catégorie de produits la plus achetée
plt.subplot(2, 2, 2)
sns.countplot(x='Most Purchased Category', data=metrics_df, palette='viridis')
plt.title('Distribution de la Catégorie de Produits la Plus Achetée')
plt.xlabel('Catégorie de Produits')
plt.ylabel('Nombre de Clients')

# Nombre de ventes par mois
plt.subplot(2, 1, 2)
sales_per_month.plot(kind='line', marker='o')
plt.title('Nombre de ventes par mois')
plt.xlabel('Mois')
plt.ylabel('Nombre de ventes')
plt.grid(True)

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='categ', y='price', data=cleaned_data)
plt.title('Dispersion des prix par catégorie de produits')
plt.xlabel('Catégorie')
plt.ylabel('Prix')
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='age', y='sex', data=cleaned_data)
plt.title('sex par age')
plt.xlabel('age')
plt.ylabel('sex')
plt.grid(True)
plt.show()



