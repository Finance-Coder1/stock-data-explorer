"""
stock_analyzer.py

This module analyzes stock data using yfinance and matplotlib.
It fetches historical data, calculates summary statistics, and
visualizes trends in a user-friendly format.
"""

import datetime
import sys
import os
import csv
import yfinance as yf
import matplotlib.pyplot as plt


def main():
    """
    Functionality:
    Main function that collates all code and calls functions.
    This function has most or all menus part of the program.
    """
    all_stocks = []
    summary_statistics_titles = [
        "Company: ",
        "Date Range: ",
        "Total Trading Days: ",
        "Opening Price: ",
        "Closing Price: ",
        "Average Closing Price: ",
        "Highest Closing Price: ",
        "Highest Intraday Price: ",
        "Lowest Closing Price: ",
        "Lowest Intraday Price: ",
        "Daily Price Volatility: ",
        "Annualized Price Volatility: ",
        "Total Return (%): ",
        "Average Daily Volume: ",
    ]
    while True:
        print("-------------------------")
        print("Welcome to Stock Data Explorer!")

        print(
            "\nMenu:\n1. Analyze a Stock\n2. Access All Analyzed Stocks\n3. User Guide\n4. Exit\n---------------"
        )

        while True:
            try:
                main_menu_choice = int(
                    input("What would you like to do? (1, 2, 3, 4): ").strip()
                )
                if 1 <= main_menu_choice <= 4:
                    break
                print("Invalid input, please choose between 1 and 4")
            except ValueError:
                print("Invalid input, please try again.")

        print("--------------------------")

        if main_menu_choice == 1:
            stock_data = analyze_stock(all_stocks, summary_statistics_titles)
            while True:
                print("\n----------------------------------\n")
                print(
                    "Stock Analysis Menu:\n1. Save Data to CSV\n2. Analyze Another Stock\n3. Return to Main Menu\n4. Exit"
                )

                while True:
                    try:
                        stock_choice = int(
                            input(
                                "What would you like to do? (1, 2, 3, or 4): "
                            ).strip()
                        )
                        if 1 <= stock_choice <= 4:
                            break
                        print("Invalid input, please choose between 1 and 4")
                    except ValueError:
                        print("Invalid input, please try again.")
                if stock_choice == 1:
                    save_one_stock_to_csv(stock_data, summary_statistics_titles)
                    continue
                elif stock_choice == 2:
                    print()
                    stock_data = analyze_stock(all_stocks, summary_statistics_titles)
                elif stock_choice == 3:
                    break
                else:
                    exit_menu()

        elif main_menu_choice == 2:
            if not all_stocks:
                print(
                    "\n**You must first analyze one or more stocks before you can access them.**\n"
                )
                continue

            while True:
                print(
                    "\nStock Access Menu:\n1. List All Analyzed Stocks\n2. Save All Analyzed Stocks to CSV\n3. View Graphs of Individual Analyzed Stocks\n4. Return to Main Menu\n5. Exit\n---------------"
                )

                while True:
                    try:
                        access_choice = int(
                            input(
                                "What would you like to do? (1, 2, 3, 4, or 5): "
                            ).strip()
                        )
                        if 1 <= access_choice <= 5:
                            break
                        else:
                            print("Invalid input, please choose between 1 and 5")
                    except ValueError:
                        print("Invalid input. Please try again.")
                if access_choice == 1:
                    list_stocks(all_stocks, summary_statistics_titles)
                elif access_choice == 2:
                    save_all_to_csv(all_stocks, summary_statistics_titles)
                    continue
                elif access_choice == 3:
                    if view_stock_graph(all_stocks):
                        break
                    continue
                elif access_choice == 4:
                    break
                else:
                    exit_menu()
        elif main_menu_choice == 3:
            print("""
    ----------------------------------
    User Guide:
    1. Select 'Analyze a Stock' to input a ticker symbol and date range.
    2. Dates must be entered in YYYY-MM-DD format and be within valid trading days.
    3. After analysis, choose to save data or analyze another stock.
    4. Saved CSV files can be found in the same folder.
    5. Select 'Access All Analyzed Stocks' to do the following:
            I. List All Analyzed Stocks
            II. Save All Analyzed Stocks to a CSV
            III. View Graphs of Individual Analyzed Stocks
                
    *To exit at any point, follow the prompts in any menu*
    ----------------------------------
            """)
        else:
            exit_menu()


def analyze_stock(all_stocks, summary_statistics_titles):
    """
    Functionality:
    Asks user for stock and date range, validates both(through calling functions), and prints all the statistics
    This function also saves the stock and its statistics to a global list of dictionaries

    Returns:
    - Dictionary with the stock and its statistics
    """

    while True:
        if not (
            stock_ticker := validate_ticker(
                input("Please enter a stock ticker: ").strip().upper()
            )
        ):
            continue
        if not (
            start_date := validate_date(
                input("Please enter a start date(YYYY-MM-DD): ").strip()
            )
        ):
            continue
        if not (
            end_date := validate_date(
                input("Please enter an end date(YYYY-MM-DD): ").strip()
            )
        ):
            continue

        print("\n.....Validating.....\n")

        if start_date >= end_date:
            print("Start date must occur before end date")
            continue
        if start_date > datetime.date.today() or end_date > datetime.date.today():
            print("Date(s) entered cannot be in the future.")
            continue

        print("-----------------------------")
        if not (
            summary_statistics := stock_summary_statistics(
                stock_ticker, start_date, end_date
            )
        ):
            print(
                "There is no data available for this date range.\nPlease try again with another set of dates.\n-----------------------------"
            )
            continue

        print(f"Company: {stock_ticker['ticker']} ({stock_ticker['long_name']})")
        print(f"Valid Date Range: {start_date} to {end_date}")
        print("----------------------------------\n")
        print(
            "--\n**Note**:\nIf either the start or end date occurs on a day when the market was closed, the soonest succeeding day was chosen.\n--\n"
        )

        for i in range(len(summary_statistics)):
            print(f"{summary_statistics_titles[i]}{summary_statistics[f'stat{i + 1}']}")

        if all_stocks:
            for stock in all_stocks:
                if (
                    stock["stat1"] == summary_statistics["stat1"]
                    and stock["stat2"] == summary_statistics["stat2"]
                ):
                    return summary_statistics

        all_stocks.append(summary_statistics)

        return summary_statistics


def validate_date(d):
    """
    Functionality:
    Validates the date entered by user

    Returns:
    - None if the user enters an invalid date
    - Date object with year, month, and day
    """

    try:
        return datetime.datetime.strptime(d, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format or invalid calendar date.")
        return None


def validate_ticker(t):
    """
    Functionality:
    Validates whether or not the ticker is valid

    Returns:
    - None if the entered ticker doesn't exist
    - a dictionary with the ticker symbol and the company name
    """

    original_stderr = sys.stderr
    sys.stderr = open(os.devnull, "w")
    stock = yf.Ticker(t)

    if not stock.info or stock.info.get("longName") is None:
        sys.stderr.close()
        sys.stderr = original_stderr
        print("Entered ticker does not exist.")
        return None

    sys.stderr.close()
    sys.stderr = original_stderr
    return {"ticker": t, "long_name": stock.info.get("longName")}


def stock_summary_statistics(ticker, start_date, end_date):
    """
    Functionality:
    Calculates all of the statistics of the given stock and stores them in a dictionary

    Returns:
    - None if no data for the given ticker or the date range could be found
    - sum_stats, a dictionary that contains all the calculated statistics for the given stock and its date range
    """
    sum_stats = {}

    stock = yf.Ticker(ticker["ticker"])
    data = stock.history(start=start_date, end=end_date)
    if data.empty:
        return None

    # saving ticker to dict
    sum_stats["stat1"] = f"{ticker['ticker']} ({ticker['long_name']})"
    # saving date range to dict
    sum_stats["stat2"] = f"{data.index[0].date()} to {data.index[-1].date()}"
    # saving number of trading days
    sum_stats["stat3"] = f"{len(data):,}"
    # saving opening price to dict
    sum_stats["stat4"] = f"${data.iloc[0]['Open']:,.2f}"
    # saving closing price to dict
    sum_stats["stat5"] = f"${data.iloc[-1]['Close']:,.2f}"
    # saving average closing price to dict
    sum_stats["stat6"] = f"${data['Close'].mean():,.2f}"
    # saving highest closing price to dict
    sum_stats["stat7"] = f"${data['Close'].max():,.2f}"
    # saving highest intraday price to dict
    sum_stats["stat8"] = f"${data['High'].max():,.2f}"
    # saving lowest closing price to dict
    sum_stats["stat9"] = f"${data['Close'].min():,.2f}"
    # saving lowest intraday price to dict
    sum_stats["stat10"] = f"${data['Low'].min():,.2f}"
    # saving daily price volatility to dict
    returns = data["Close"].pct_change().dropna()
    sum_stats["stat11"] = f"{returns.std():,.6f}"
    # saving annualized price volatility to dict
    sum_stats["stat12"] = f"{(returns.std() * (252**0.5)):,.6f}"
    # saving total return to dict
    sum_stats["stat13"] = (
        f"{((data.iloc[-1]['Close'] - data.iloc[0]['Open']) / data.iloc[0]['Open']) * 100:,.4f}%"
    )
    # saving average daily volume to dict
    sum_stats["stat14"] = f"{round(data['Volume'].mean()):,}"

    return sum_stats


def save_one_stock_to_csv(sum_stats, summary_statistics_titles):
    """
    Functionality:
    Saves the current stock being analyzed to its own CSV file with its statistics
    This function creates a CSV file named based on the stock ticker and the date range

    Returns:
    - None if the user attempts the same stock with the same date range twice
    - None if the function executes in its entirety
    """

    cleaned_titles = [
        title.strip(": ").lower().replace(" ", "_")
        for title in summary_statistics_titles
    ]
    filename = (
        f"{sum_stats['stat1'].split(' ')[0]}_{sum_stats['stat2'].replace(' ', '_')}.csv"
    )
    new_row = {
        title: sum_stats[f"stat{i + 1}"] for i, title in enumerate(cleaned_titles)
    }

    file_exists = False
    duplicate = False

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            file_exists = True
            for row in reader:
                if row["date_range"] == new_row["date_range"]:
                    duplicate = True
                    break
    except FileNotFoundError:
        file_exists = False

    if duplicate:
        print(
            f"\n--\nStock data for {sum_stats['stat1']} from {sum_stats['stat2']} is already saved in {filename}.\n--"
        )
        return

    with open(filename, "a", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=cleaned_titles)
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_row)

    print("\n.....Saving.....\n")
    print(f"Data saved to {filename}")


def list_stocks(all_stocks, summary_statistics_titles):
    """
    Functionality:
    Accesses all analyzed stocks so far and prints them along with all their statistics

    Returns:
    - None if the function executes in its entirety
    """

    print("\nAll Analyzed Stocks:\n-----****-----")
    for stock in all_stocks:
        for i in range(len(stock)):
            print(f"{summary_statistics_titles[i]}{stock[f'stat{i + 1}']}")
        print("--\n")


def save_all_to_csv(all_stocks, summary_statistics_titles):
    """
    Functionality:
    Accesses all analyzed stocks so far and their statistics and saves them to a CSV file
    This function creates and names a csv file to the user's discretion

    Returns:
    - None
    """

    rows = []

    cleaned_titles = [
        title.strip(": ").lower().replace(" ", "_")
        for title in summary_statistics_titles
    ]

    filename = ""
    while not filename:
        filename = input("Please enter a filename: ").strip()
    if not filename.endswith(".csv"):
        filename += ".csv"
    if " " in filename:
        filename = filename.replace(" ", "_")

    for j in range(len(all_stocks)):
        rows.append(
            {
                title: all_stocks[j][f"stat{i + 1}"]
                for i, title in enumerate(cleaned_titles)
            }
        )

    file_exists = False

    try:
        with open(filename, "r", encoding="utf-8") as file:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(filename, "a", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=cleaned_titles)
        if not file_exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print("\n.....Saving.....\n")
    print(f"Data saved to {filename}")


def view_stock_graph(all_stocks):
    """
    Functionality:
    Allows the user to select and graph a statistic for a previously analyzed stock.

    Returns:
    - True if the user chooses to return to the main menu
    - False if they return to the stock access menu or complete a graph
    - Exits the program if the user chooses to exit
    """

    print("---------------\nBelow are all of the stocks you have analyzed:")
    for i in range(len(all_stocks)):
        print(f"{i + 1}. {all_stocks[i]['stat1']} ~ {all_stocks[i]['stat2']}")
    print(
        f"{len(all_stocks) + 1}. Return to Stock Access Menu\n{len(all_stocks) + 2}. Return to Main Menu\n{len(all_stocks) + 3}. Exit"
    )

    print()

    while True:
        try:
            stock_number = int(
                input(
                    "Which stock would you like to view? (Enter the Number): "
                ).strip()
            )
            if not 1 <= stock_number <= len(all_stocks) + 3:
                print(
                    f"Invalid input. You must input a number between 1 and {len(all_stocks) + 3}"
                )
                continue
        except ValueError:
            print("Invalid input. Please try again.")
            continue
        else:
            if stock_number == len(all_stocks) + 1:
                return False
            if stock_number == len(all_stocks) + 2:
                return True
            if stock_number == len(all_stocks) + 3:
                exit_menu()
                continue
        break

    stock = yf.Ticker(all_stocks[stock_number - 1]["stat1"].split(" ")[0])
    start_date, end_date = all_stocks[stock_number - 1]["stat2"].split(" to ")
    data = stock.history(start=start_date, end=end_date)

    print("\n.....Retrieving Stock.....\n")

    print(
        f"Available Statistics for {all_stocks[stock_number - 1]['stat1']} from {all_stocks[stock_number - 1]['stat2']}"
    )
    print(
        "1. Daily Opening Price\n2. Daily Closing Price\n3. Highest Intraday Price\n4. Lowest Intraday Price\n5. Daily Volume"
    )

    while True:
        try:
            graph_stat = int(
                input(
                    "Which statistic do you want to graph? (1, 2, 3, 4, or 5): "
                ).strip()
            )
            if 1 <= graph_stat <= 5:
                break
            print("Invalid Input. Please enter a number between 1 and 5")
        except ValueError:
            print("Invalid Input. Please try again.")

    stat_options = {1: "Open", 2: "Close", 3: "High", 4: "Low", 5: "Volume"}

    graph_options = {
        1: "Opening Price",
        2: "Closing Price",
        3: "High Price",
        4: "Low Price",
        5: "Volume",
    }

    print("\n.....Graphing.....\n")

    plt.figure(figsize=(10, 5))
    if graph_stat != 5:
        plt.plot(
            data.index,
            data[stat_options[graph_stat]],
            label=graph_options[graph_stat],
            color="blue",
        )
    else:
        plt.bar(
            data.index,
            data[stat_options[graph_stat]],
            label=graph_options[graph_stat],
            color="gray",
            width=0.8,
        )
    plt.title(
        f"{all_stocks[stock_number - 1]['stat1']} {graph_options[graph_stat]} from {start_date} to {end_date}"
    )
    plt.xlabel("Date")
    if graph_stat != 5:
        plt.ylabel("Price ($)")
    else:
        plt.ylabel("Volume")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    return False


def exit_menu():
    """
    Functionality:
    Prompts user for certainty over leaving

    Returns:
    - None if user cancels
    - calls sys.exit() if user confirms
    """

    exit_choice = (
        input("Are you sure you wish to exit? All analyzed stocks will be lost [y/N]: ")
        .strip()
        .lower()
    )
    while True:
        if exit_choice == "y":
            sys.exit("\n.....Exiting.....\n")
        elif exit_choice == "n":
            return
        else:
            exit_choice = input("Invalid input. Please try again: ").strip().lower()


if __name__ == "__main__":
    main()
