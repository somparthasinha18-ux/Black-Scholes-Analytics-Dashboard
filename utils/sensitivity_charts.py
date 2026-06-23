import numpy as np
import plotly.graph_objects as go

from utils.greeks import calculate_greeks


BACKGROUND_COLOR = "#0b1221"
GRID_COLOR = "#24324a"
TEXT_COLOR = "#f8fafc"

CALL_COLOR = "#22c55e"
PUT_COLOR = "#ef4444"
GAMMA_COLOR = "#38bdf8"
VEGA_COLOR = "#a855f7"
THETA_CALL_COLOR = "#f59e0b"
THETA_PUT_COLOR = "#60a5fa"


def _base_layout(title, x_title, y_title):
    """
    Common Plotly layout used by all sensitivity charts.
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


def _chart_html(fig, include_plotlyjs=False):
    """
    Convert Plotly figure into embeddable HTML.
    """

    return fig.to_html(
        full_html=False,
        include_plotlyjs=include_plotlyjs,
        config={
            "displayModeBar": True,
            "responsive": True
        }
    )


def delta_sensitivity_chart(S, K, T, r, sigma):
    """
    Plot Call Delta and Put Delta against stock price.
    """

    stock_prices = np.linspace(S * 0.5, S * 1.5, 80)

    delta_call = []
    delta_put = []

    for price in stock_prices:

        greeks = calculate_greeks(
            price,
            K,
            T,
            r,
            sigma
        )

        delta_call.append(greeks["delta_call"])
        delta_put.append(greeks["delta_put"])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock_prices,
            y=delta_call,
            mode="lines",
            name="Call Delta",
            line=dict(
                width=4,
                color=CALL_COLOR
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock_prices,
            y=delta_put,
            mode="lines",
            name="Put Delta",
            line=dict(
                width=4,
                color=PUT_COLOR
            )
        )
    )

    fig.add_vline(
        x=S,
        line_width=2,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Current S",
        annotation_position="top"
    )

    fig.update_layout(
        **_base_layout(
            "Delta Sensitivity vs Stock Price",
            "Underlying Stock Price",
            "Delta"
        )
    )

    return _chart_html(fig)


def gamma_sensitivity_chart(S, K, T, r, sigma):
    """
    Plot Gamma against stock price.
    """

    stock_prices = np.linspace(S * 0.5, S * 1.5, 80)

    gamma_values = []

    for price in stock_prices:

        greeks = calculate_greeks(
            price,
            K,
            T,
            r,
            sigma
        )

        gamma_values.append(greeks["gamma"])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock_prices,
            y=gamma_values,
            mode="lines",
            name="Gamma",
            line=dict(
                width=4,
                color=GAMMA_COLOR
            )
        )
    )

    fig.add_vline(
        x=S,
        line_width=2,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Current S",
        annotation_position="top"
    )

    fig.update_layout(
        **_base_layout(
            "Gamma Sensitivity vs Stock Price",
            "Underlying Stock Price",
            "Gamma"
        )
    )

    return _chart_html(fig)


def vega_sensitivity_chart(S, K, T, r, sigma):
    """
    Plot Vega against volatility.
    """

    volatility_range = np.linspace(
        max(1, sigma * 0.25),
        min(150, sigma * 2.0),
        80
    )

    vega_values = []

    for volatility in volatility_range:

        greeks = calculate_greeks(
            S,
            K,
            T,
            r,
            volatility
        )

        vega_values.append(greeks["vega"])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=volatility_range,
            y=vega_values,
            mode="lines",
            name="Vega",
            line=dict(
                width=4,
                color=VEGA_COLOR
            )
        )
    )

    fig.add_vline(
        x=sigma,
        line_width=2,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Current Vol",
        annotation_position="top"
    )

    fig.update_layout(
        **_base_layout(
            "Vega Sensitivity vs Volatility",
            "Volatility (%)",
            "Vega"
        )
    )

    return _chart_html(fig)


def theta_sensitivity_chart(S, K, T, r, sigma):
    """
    Plot Call Theta and Put Theta against time to expiry.
    """

    time_range = np.linspace(0.01, max(2.0, T * 2), 80)

    theta_call = []
    theta_put = []

    for time in time_range:

        greeks = calculate_greeks(
            S,
            K,
            time,
            r,
            sigma
        )

        theta_call.append(greeks["theta_call"])
        theta_put.append(greeks["theta_put"])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time_range,
            y=theta_call,
            mode="lines",
            name="Call Theta",
            line=dict(
                width=4,
                color=THETA_CALL_COLOR
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=time_range,
            y=theta_put,
            mode="lines",
            name="Put Theta",
            line=dict(
                width=4,
                color=THETA_PUT_COLOR
            )
        )
    )

    fig.add_vline(
        x=T,
        line_width=2,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Current T",
        annotation_position="top"
    )

    fig.update_layout(
        **_base_layout(
            "Theta Sensitivity vs Time to Expiry",
            "Time to Expiry (Years)",
            "Theta"
        )
    )

    return _chart_html(fig)


def generate_sensitivity_charts(S, K, T, r, sigma):
    """
    Generate all Greeks sensitivity charts.
    """

    return {
        "delta": delta_sensitivity_chart(
            S,
            K,
            T,
            r,
            sigma
        ),

        "gamma": gamma_sensitivity_chart(
            S,
            K,
            T,
            r,
            sigma
        ),

        "vega": vega_sensitivity_chart(
            S,
            K,
            T,
            r,
            sigma
        ),

        "theta": theta_sensitivity_chart(
            S,
            K,
            T,
            r,
            sigma
        )
    }