import yfinance as yf
import numpy as np


def get_market_data(ticker):
    """
    Fetch market data from Yahoo Finance.

    Returns:
        dict or None
    """

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

        history = stock.history(period="6mo")

        if history.empty:
            return None

        current_price = round(
            history["Close"].iloc[-1],
            2
        )

        previous_close = round(
            history["Close"].iloc[-2],
            2
        )

        daily_return = round(
            (
                (current_price - previous_close)
                / previous_close
            ) * 100,
            2
        )

        returns = np.log(
            history["Close"]
            /
            history["Close"].shift(1)
        )

        historical_volatility = round(
            returns.std() * np.sqrt(252) * 100,
            2
        )

        return {
            "ticker": ticker.upper(),
            "company_name": info.get(
                "shortName",
                ticker.upper()
            ),
            "current_price": current_price,
            "previous_close": previous_close,
            "daily_return": daily_return,
            "historical_volatility": historical_volatility
        }

    except Exception:
        return None