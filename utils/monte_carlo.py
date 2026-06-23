import numpy as np
import plotly.graph_objects as go


BACKGROUND_COLOR = "#0b1221"
GRID_COLOR = "#24324a"
TEXT_COLOR = "#f8fafc"
HIST_COLOR = "#38bdf8"


def monte_carlo_option_pricing(
    S,
    K,
    T,
    r,
    sigma,
    simulations=10000,
    random_seed=42
):
    """
    Price European options using Monte Carlo simulation.

    Parameters:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to expiry in years
        r (float): Risk-free rate in percent
        sigma (float): Volatility in percent
        simulations (int): Number of simulated paths

    Returns:
        dict: Monte Carlo call/put prices and terminal price chart
    """

    np.random.seed(random_seed)

    r_decimal = r / 100
    sigma_decimal = sigma / 100

    z = np.random.standard_normal(simulations)

    terminal_prices = S * np.exp(
        (r_decimal - 0.5 * sigma_decimal ** 2) * T
        + sigma_decimal * np.sqrt(T) * z
    )

    call_payoffs = np.maximum(terminal_prices - K, 0)
    put_payoffs = np.maximum(K - terminal_prices, 0)

    discount_factor = np.exp(-r_decimal * T)

    call_price = discount_factor * np.mean(call_payoffs)
    put_price = discount_factor * np.mean(put_payoffs)

    chart = terminal_price_distribution_chart(
        terminal_prices,
        K
    )

    return {
        "call_price": round(call_price, 4),
        "put_price": round(put_price, 4),
        "call_display": round(call_price, 2),
        "put_display": round(put_price, 2),
        "simulations": simulations,
        "mean_terminal_price": round(float(np.mean(terminal_prices)), 2),
        "std_terminal_price": round(float(np.std(terminal_prices)), 2),
        "chart": chart
    }


def terminal_price_distribution_chart(terminal_prices, K):
    """
    Plot terminal stock price distribution.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=terminal_prices,
            nbinsx=60,
            name="Terminal Prices",
            marker=dict(
                color=HIST_COLOR,
                line=dict(
                    color="#0f172a",
                    width=1
                )
            ),
            opacity=0.85
        )
    )

    fig.add_vline(
        x=K,
        line_width=3,
        line_dash="dash",
        line_color="#f59e0b",
        annotation_text="Strike Price",
        annotation_position="top"
    )

    fig.update_layout(
        title={
            "text": "Monte Carlo Terminal Price Distribution",
            "x": 0.5,
            "font": {
                "size": 18,
                "color": TEXT_COLOR
            }
        },
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font={
            "color": TEXT_COLOR,
            "family": "Poppins"
        },
        xaxis={
            "title": "Terminal Stock Price",
            "gridcolor": GRID_COLOR,
            "zerolinecolor": GRID_COLOR
        },
        yaxis={
            "title": "Frequency",
            "gridcolor": GRID_COLOR,
            "zerolinecolor": GRID_COLOR
        },
        bargap=0.05,
        margin={
            "l": 60,
            "r": 30,
            "t": 70,
            "b": 60
        },
        template="plotly_dark"
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config={
            "displayModeBar": True,
            "responsive": True
        }
    )