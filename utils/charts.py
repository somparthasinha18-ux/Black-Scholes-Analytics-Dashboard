import numpy as np
import plotly.graph_objects as go

from utils.black_scholes import black_scholes


BACKGROUND_COLOR = "#0b1221"
GRID_COLOR = "#24324a"
TEXT_COLOR = "#f8fafc"
CALL_COLOR = "#22c55e"
PUT_COLOR = "#f59e0b"
PAYOFF_COLOR = "#38bdf8"


def _base_layout(title, x_title, y_title):
    """
    Common Plotly layout for dashboard charts.
    """

    return {
        "title": {
            "text": title,
            "x": 0.5,
            "font": {
                "size": 18,
                "color": TEXT_COLOR
            }
        },
        "paper_bgcolor": BACKGROUND_COLOR,
        "plot_bgcolor": BACKGROUND_COLOR,
        "font": {
            "color": TEXT_COLOR,
            "family": "Poppins"
        },
        "xaxis": {
            "title": x_title,
            "gridcolor": GRID_COLOR,
            "zerolinecolor": GRID_COLOR
        },
        "yaxis": {
            "title": y_title,
            "gridcolor": GRID_COLOR,
            "zerolinecolor": GRID_COLOR
        },
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "center",
            "x": 0.5
        },
        "margin": {
            "l": 60,
            "r": 30,
            "t": 70,
            "b": 60
        },
        "template": "plotly_dark"
    }


def option_price_chart(K, T, r, sigma):
    """
    Generate option price chart across a range of stock prices.
    """

    stock_prices = np.linspace(K * 0.5, K * 1.5, 100)

    call_prices = []
    put_prices = []

    for stock_price in stock_prices:

        call_price, put_price = black_scholes(
            stock_price,
            K,
            T,
            r,
            sigma
        )

        call_prices.append(call_price)
        put_prices.append(put_price)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock_prices,
            y=call_prices,
            mode="lines",
            name="Call Price",
            line=dict(
                width=4,
                color=CALL_COLOR
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock_prices,
            y=put_prices,
            mode="lines",
            name="Put Price",
            line=dict(
                width=4,
                color=PUT_COLOR
            )
        )
    )

    fig.add_vline(
        x=K,
        line_width=2,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Strike",
        annotation_position="top"
    )

    fig.update_layout(
        **_base_layout(
            "Option Price vs Stock Price",
            "Underlying Stock Price",
            "Option Price"
        )
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn",
        config={
            "displayModeBar": True,
            "responsive": True
        }
    )


def payoff_chart(K):
    """
    Generate European call and put payoff diagram at expiry.
    """

    stock_prices = np.linspace(K * 0.5, K * 1.5, 100)

    call_payoff = np.maximum(stock_prices - K, 0)
    put_payoff = np.maximum(K - stock_prices, 0)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock_prices,
            y=call_payoff,
            mode="lines",
            name="Call Payoff",
            line=dict(
                width=4,
                color=CALL_COLOR
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock_prices,
            y=put_payoff,
            mode="lines",
            name="Put Payoff",
            line=dict(
                width=4,
                color=PAYOFF_COLOR
            )
        )
    )

    fig.add_vline(
        x=K,
        line_width=2,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Strike",
        annotation_position="top"
    )

    fig.add_hline(
        y=0,
        line_width=1,
        line_color="#475569"
    )

    fig.update_layout(
        **_base_layout(
            "Payoff Diagram at Expiry",
            "Underlying Stock Price at Expiry",
            "Payoff"
        )
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        config={
            "displayModeBar": True,
            "responsive": True
        }
    )