# Standard library imports
import os
from datetime import datetime, timedelta
from pathlib import Path

# Third-party library imports
import requests  # pip install requests
from dotenv import load_dotenv  # pip install python-dotenv
import yfinance as yf  # pip install yfinance
import yagmail  # pip install yagmail
import matplotlib.pyplot as plt  # pip install matplotlib
import pandas as pd  # pip install pandas
from bs4 import BeautifulSoup  # pip install beautifulsoup4


# Load environment variables from .env file
def load_environment_variables():
    """Load environment variables from the .env file."""
    try:
        script_dir = Path(__file__).resolve().parent
    except NameError:
        script_dir = Path(os.getcwd())
    env_file_path = script_dir / ".env"
    load_dotenv(env_file_path)


# Mapping of company names to ticker symbols
# Put simple names for the companies you want to track so the queries to the NewsAPI are more likely to return relevant results
stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
}

etfs = {
    "MSCI World": "IWDA.AS",
    "S&P 500": "SXR8.DE",
}

currencies = {
    "EUR/USD": "EURUSD=X",
}

commodities = {
    "Gold": "GC=F",
}

crypto = {
    "BitCoin": "BTC-USD",
}


def get_info(tickers, category):
    """Fetch the daily percentage change, total value, and PER for a list of tickers."""
    info = {}
    total_value = 0
    for company_name, ticker in tickers.items():
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        if not hist.empty and len(hist) >= 2:
            yesterday_info = hist.iloc[-2]
            variation = yesterday_info["Close"] / yesterday_info["Open"] - 1
            per = stock.info.get("trailingPE", "N/A") if category == "Stocks" else "N/A"
            info[company_name] = {
                "variation": variation,
                "close": yesterday_info["Close"],
                "per": per,
            }
            total_value += yesterday_info["Close"]
        else:
            info[company_name] = "No data"
    return info, total_value


def get_stock_info():
    """Fetch the daily percentage change for a list of stocks and calculate the simple average.
    --> Unweighted average as if each ticker has the same weight in the portfolio."""
    categories = {
        "Stocks": stocks,
        "ETFs": etfs,
        "Currencies": currencies,
        "Commodities": commodities,
        "Crypto": crypto,
    }

    total_info = {}
    category_averages = {}

    for category, tickers in categories.items():
        info, _ = get_info(tickers, category)
        total_info.update(info)

        variations = [
            stock_info["variation"]
            for stock_info in info.values()
            if isinstance(stock_info, dict)
        ]

        if variations:
            category_averages[category] = sum(variations) / len(variations)
        else:
            category_averages[category] = 0

    total_variations = [
        stock_info["variation"]
        for stock_info in total_info.values()
        if isinstance(stock_info, dict)
    ]

    if total_variations:
        total_average = sum(total_variations) / len(total_variations)
    else:
        total_average = 0

    return total_info, category_averages, total_average


def get_earnings_dates():
    """Fetch the most recent and next future earnings dates for a list of stocks."""
    results = {}
    for company_name, ticker in stocks.items():
        stock = yf.Ticker(ticker)
        earnings_data = stock.get_earnings_dates()
        earnings_data.index = pd.to_datetime(earnings_data.index.astype(str).str[:10])
        today = datetime.now().date()
        past_earnings = earnings_data[earnings_data.index.date <= today].sort_index(
            ascending=False
        )
        future_earnings = earnings_data[earnings_data.index.date > today].sort_index()
        most_recent_earning = past_earnings.iloc[0] if not past_earnings.empty else None
        next_future_earning = (
            future_earnings.iloc[0] if not future_earnings.empty else None
        )
        results[company_name] = {
            "most_recent": most_recent_earning,
            "next_future": next_future_earning,
        }
    return results


def plot_small_charts(tickers):
    """Plot small charts for each ticker and save them as images."""
    chart_paths = {}
    charts_dir = Path("./charts")
    charts_dir.mkdir(exist_ok=True)

    plt.style.use("dark_background")  # dark theme like my heart 🖤🥀⛓

    for company_name, ticker in tickers.items():
        data = yf.download(ticker, period="1mo")
        plt.figure(figsize=(2, 1))
        plt.plot(data["Close"])
        plt.xticks([])
        plt.yticks([])
        chart_path = charts_dir / f"{ticker}_chart.png"
        plt.savefig(chart_path, dpi=300)
        plt.close()
        chart_paths[company_name] = chart_path

    return chart_paths


# Get news with News API
def get_news(news_api_key):
    """Fetch the latest news articles for each ticker individually."""
    tickers = {**stocks, **etfs, **currencies, **commodities, **crypto}
    news_info = {}

    date_from = (datetime.now() - timedelta(days=7)).isoformat()

    for company_name, ticker in tickers.items():

        def fetch_news(page_size):
            params = {
                "apiKey": news_api_key,
                "q": f'"{company_name}"',
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": page_size,
                "from": date_from,
            }
            response = requests.get("https://newsapi.org/v2/everything", params=params)
            response.raise_for_status()
            return response.json()["articles"]

        try:
            news_items = fetch_news(1)

            if news_items and (
                news_items[0].get("title") == "[Removed]"
                or news_items[0].get("description") == "[Removed]"
            ):
                news_items = fetch_news(3)

            valid_item_found = False
            for item in news_items:
                if (
                    item.get("title") != "[Removed]"
                    and item.get("description") != "[Removed]"
                ):
                    news_info[company_name] = {
                        "title": item.get("title", "No title provided"),
                        "description": item.get(
                            "description", "No description provided"
                        ),
                        "url": item.get("url", "No URL provided"),
                    }
                    valid_item_found = True
                    break

            if not valid_item_found:
                news_info[company_name] = {
                    "title": "No relevant news available",
                    "description": "",
                    "url": "",
                }
        except requests.RequestException as e:
            news_info[company_name] = {
                "title": "News information is currently unavailable.",
                "description": f"Error: {e}",
                "url": "",
            }

    return news_info


def generate_html_table(
    stock_info, earnings_info, news_info, chart_paths, category_averages, total_average
):
    """Generate an HTML table that combines all information for each stock."""
    table_html = """
    <table border="1" style="border-collapse: collapse; width: 100%; table-layout: fixed;">
        <thead>
            <tr>
                <th style="padding: 4px;">Ticker</th>
                <th style="padding: 4px;">Variation (%)</th>
                <th style="padding: 4px;">PER</th>
                <th style="padding: 4px;">Most Recent Earning</th>
                <th style="padding: 4px;">Next Future Earning</th>
                <th style="padding: 4px;">Chart (30 days period)</th>
            </tr>
        </thead>
        <tbody>
    """
    categories = {
        "Stocks": stocks,
        "ETFs": etfs,
        "Currencies": currencies,
        "Commodities": commodities,
        "Crypto": crypto,
    }

    for category, tickers in categories.items():
        table_html += f"""
        <tr>
            <td colspan="6" style="padding: 8px; text-align:center; font-size: 1.2em;"><strong>{category} - Unweighted Average Variation: {category_averages[category]*100:.2f}%</strong></td>
        </tr>
        """
        for company_name, info in stock_info.items():
            if company_name in tickers:
                if isinstance(info, dict):
                    most_recent = earnings_info.get(company_name, {}).get("most_recent")
                    next_future = earnings_info.get(company_name, {}).get("next_future")
                    most_recent_earning = (
                        f"Date: {most_recent.name.date()}<br>EPS Estimate: {most_recent.get('EPS Estimate', 'N/A')}<br>Reported EPS: {most_recent.get('Reported EPS', 'N/A')}"
                        if most_recent is not None
                        else "N/A"
                    )
                    next_future_earning = (
                        f"Date: {next_future.name.date()}<br>EPS Estimate: {next_future.get('EPS Estimate', 'N/A')}<br>Reported EPS: {next_future.get('Reported EPS', 'N/A')}"
                        if next_future is not None
                        else "N/A"
                    )
                    table_html += f"""
                    <tr>
                        <td style='text-align:center; padding: 4px;'><strong>{company_name}</strong></td>
                        <td style='text-align:center; padding: 4px;'>{info['variation']*100:.2f}</td>
                        <td style='text-align:center; padding: 4px;'>{info['per']}</td>
                        <td style='text-align:center; padding: 4px;'>{most_recent_earning}</td>
                        <td style='text-align:center; padding: 4px;'>{next_future_earning}</td>
                        <td style='text-align:center; padding: 4px;'><img src='cid:{chart_paths[company_name].name}' alt='{company_name} chart'></td>
                    </tr>
                    """
                    news = news_info.get(company_name, {})
                    news_html = f"""
                    <tr>
                        <td colspan='6' style='text-align:left; padding: 4px;'>
                            <strong>News:</strong> <a href='{news.get('url', '')}'>{news.get('title', '')}</a><br>
                            {news.get('description', '')}
                        </td>
                    </tr>
                    """
                    table_html += news_html
                else:
                    table_html += f"""
                    <tr>
                        <td style='text-align:center; padding: 4px;'><strong>{company_name}</strong></td>
                        <td colspan='5' style='text-align:center; padding: 4px;'>{info}</td>
                    </tr>
                    """
    table_html += f"""
        </tbody>
        <tfoot>
            <tr>
                <td colspan="6" style="padding: 8px; text-align:center; font-size: 1.4em;"><strong>Total Unweighted Average Variation: {total_average*100:.2f}%</strong></td>
            </tr>
        </tfoot>
    </table>
    """
    return table_html


def format_html(html_content):
    """Format HTML content to remove unwanted spaces and gaps."""
    soup = BeautifulSoup(html_content, "html.parser")
    return (
        str(soup).replace("\n", "").replace("    ", "")
    )  # Remove unwanted spaces and gaps


def send_email(sender, password, recipient, subject, message_body, chart_paths):
    """Send an email using yagmail."""
    try:
        yag = yagmail.SMTP(sender, password)
        contents = [message_body]
        for chart_path in chart_paths.values():
            contents.append(yagmail.inline(str(chart_path)))
        yag.send(to=recipient, subject=subject, contents=contents)
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email. Error: {e}"


def main():
    load_environment_variables()

    # Check if today is Sunday (6) or Monday (0) because stock exchanges are closed the day before
    today = datetime.now().weekday()
    if today == 6 or today == 0:
        print("Today is Sunday or Monday. The script will not run.")
        return

    news_api_key = os.getenv("NEWS_API_ORG_KEY")
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    stock_info, category_averages, total_average = get_stock_info()
    earnings_info = get_earnings_dates()
    news_info = get_news(news_api_key)
    all_tickers = {**stocks, **etfs, **currencies, **commodities, **crypto}
    chart_paths = plot_small_charts(all_tickers)

    raw_message_body = f"""
        <html>
        <body style="margin: 0; padding: 0;">
            {generate_html_table(stock_info, earnings_info, news_info, chart_paths, category_averages, total_average)}
        </body>
        </html>
    """
    formatted_message_body = format_html(raw_message_body)

    with open("email_content.html", "w") as temp_file:
        temp_file.write(formatted_message_body)

    with open("email_content.html", "r") as temp_file:
        final_message_body = temp_file.read()

    print(final_message_body)
    print(chart_paths)

    email_status = send_email(
        sender,
        password,
        receiver,
        "Your Morning Stocks Update",
        final_message_body,
        chart_paths,
    )
    print(email_status)


if __name__ == "__main__":
    main()
