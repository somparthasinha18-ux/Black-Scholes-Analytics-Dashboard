from flask import Flask, render_template, request

from utils.black_scholes import black_scholes
from utils.greeks import calculate_greeks
from utils.charts import option_price_chart, payoff_chart
from utils.implied_volatility import calculate_implied_volatility
from utils.sensitivity_charts import generate_sensitivity_charts
from utils.volatility_smile import volatility_smile_chart
from utils.market_data import get_market_data
from utils.monte_carlo import monte_carlo_option_pricing
from utils.monte_carlo_paths import monte_carlo_path_chart
from utils.strategies import strategy_payoff_chart


app = Flask(__name__)


def validate_inputs(S, K, T, r, sigma):
    if S <= 0:
        return "Stock Price must be greater than 0."

    if K <= 0:
        return "Strike Price must be greater than 0."

    if T <= 0:
        return "Time to Expiry must be greater than 0."

    if sigma <= 0:
        return "Volatility must be greater than 0."

    if sigma > 500:
        return "Volatility cannot exceed 500%."

    if r < 0:
        return "Risk-Free Rate cannot be negative."

    return None


def validate_market_price(market_price):
    if market_price is not None and market_price <= 0:
        return "Market Option Price must be greater than 0."

    return None


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None
    market_data = None

    if request.method == "POST":

        try:
            ticker = request.form.get("ticker", "").strip().upper()
            strategy = request.form.get("strategy", "long_call")

            if ticker:
                market_data = get_market_data(ticker)

            S = float(request.form["stock"])
            K = float(request.form["strike"])
            sigma = float(request.form["volatility"])
            r = float(request.form["rate"])
            T = float(request.form["expiry"])
            option = request.form["option"]

            if market_data:
                S = market_data["current_price"]
                sigma = market_data["historical_volatility"]

            market_price_raw = request.form.get("market_price")
            market_price = None

            if market_price_raw:
                market_price = float(market_price_raw)

            error = validate_inputs(S, K, T, r, sigma)

            if ticker and market_data is None:
                error = "Unable to fetch market data for this ticker."

            if error is None:
                error = validate_market_price(market_price)

            if error is None:

                call_price, put_price = black_scholes(
                    S,
                    K,
                    T,
                    r,
                    sigma
                )

                greeks = calculate_greeks(
                    S,
                    K,
                    T,
                    r,
                    sigma
                )

                implied_volatility = None

                if market_price is not None:
                    implied_volatility = calculate_implied_volatility(
                        market_price=market_price,
                        S=S,
                        K=K,
                        T=T,
                        r=r,
                        option_type=option
                    )

                if abs(S - K) <= (0.01 * K):
                    status = "At The Money (ATM)"
                    status_short = "ATM"
                    badge = "warning"

                elif S > K:
                    status = "In The Money (ITM)"
                    status_short = "ITM"
                    badge = "success"

                else:
                    status = "Out of The Money (OTM)"
                    status_short = "OTM"
                    badge = "danger"

                pricing_chart = option_price_chart(
                    K,
                    T,
                    r,
                    sigma
                )

                payoff = payoff_chart(K)

                sensitivity_charts = generate_sensitivity_charts(
                    S,
                    K,
                    T,
                    r,
                    sigma
                )

                volatility_smile = volatility_smile_chart(
                    S,
                    K,
                    T,
                    r,
                    sigma,
                    option
                )

                monte_carlo = monte_carlo_option_pricing(
                    S,
                    K,
                    T,
                    r,
                    sigma
                )

                monte_carlo_paths = monte_carlo_path_chart(
                    S,
                    T,
                    r,
                    sigma
                )

                strategy_chart = strategy_payoff_chart(
                    strategy,
                    K
                )

                result = {
                    "ticker": ticker if ticker else None,
                    "stock": round(S, 2),
                    "strike": round(K, 2),
                    "volatility": round(sigma, 2),
                    "rate": round(r, 2),
                    "expiry": round(T, 4),
                    "option": option,
                    "strategy": strategy,
                    "market_price": round(market_price, 4) if market_price is not None else None,
                    "implied_volatility": round(implied_volatility * 100, 2) if implied_volatility is not None else None,
                    "call": round(call_price, 4),
                    "call_display": round(call_price, 2),
                    "put": round(put_price, 4),
                    "put_display": round(put_price, 2),
                    "status": status,
                    "status_short": status_short,
                    "badge": badge,
                    "greeks": greeks,
                    "chart": pricing_chart,
                    "payoff": payoff,
                    "sensitivity_charts": sensitivity_charts,
                    "volatility_smile": volatility_smile,
                    "market_data": market_data,
                    "monte_carlo": monte_carlo,
                    "monte_carlo_paths": monte_carlo_paths,
                    "strategy_chart": strategy_chart
                }

        except ValueError:
            error = "Please enter valid numeric values."

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        result=result,
        error=error,
        market_data=market_data
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )