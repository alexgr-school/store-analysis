from analysis.data_analyzer import DataAnalyzer
from utils.data_loader import DataLoader
from visualization.data_visualizer import DataVisualizer


def main():
    transactions_loader = DataLoader("./data/transactions.csv")
    transactions = transactions_loader.load_data()
    transactions = DataLoader.clean_transactions(transactions)

    products_loader = DataLoader("./data/products.csv")
    products = products_loader.load_data()
    products = DataLoader.clean_products(products)

    customers_loader = DataLoader("./data/customers.csv")
    customers = customers_loader.load_data()

    analyzer = DataAnalyzer(transactions, customers, products)
    complete_data = analyzer.merge_data()

    visualizer = DataVisualizer(complete_data)
    visualizer.plot_price_dispersion()
    visualizer.plot_sales_over_time()


if __name__ == "__main__":
    main()
