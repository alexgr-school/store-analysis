import os

from dotenv import load_dotenv

from analysis.data_analyzer import DataAnalyzer
from utils.data_loader import DataLoader
from visualization.data_visualizer import DataVisualizer

load_dotenv()
data_folder_path = os.getenv("DATA_FOLDER_PATH") or "./data"


def main():
    transactions_loader = DataLoader(os.path.join(data_folder_path, "transactions.csv"))
    transactions = transactions_loader.load_data()
    transactions = DataLoader.clean_transactions(transactions)

    products_loader = DataLoader(os.path.join(data_folder_path, "products.csv"))
    products = products_loader.load_data()
    products = DataLoader.clean_products(products)

    customers_loader = DataLoader(os.path.join(data_folder_path, "customers.csv"))
    customers = customers_loader.load_data()

    analyzer = DataAnalyzer(transactions, customers, products)
    complete_data = analyzer.merge_data()
    complete_data.to_csv("./output/complete_data.csv", index=False)

    visualizer = DataVisualizer(complete_data, view=False)
    # visualizer.plot_price_dispersion()
    # visualizer.plot_sales_over_time()
    # visualizer.plot_sales_per_age()
    # visualizer.plot_sales_per_age_category()
    # visualizer.plot_sales_per_sex_age()
    visualizer.plot_transaction_price_average()
    # visualizer.plot_age_dispersal()
    # visualizer.plot_products_price_lorenz_curve()
    # visualizer.plot_clients_age_lorenz_curve()
    visualizer.plot_expenses_per_age()


if __name__ == "__main__":
    main()
