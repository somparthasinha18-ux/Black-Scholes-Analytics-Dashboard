import numpy as np
import plotly.graph_objects as go

from utils.black_scholes import black_scholes
from utils.implied_volatility import calculate_implied_volatility


BACKGROUND_COLOR = "#0b1221"
GRID_COLOR = "#24324a"
TEXT_COLOR = "#f8fafc"
SMILE_COLOR = "#38bdf8"


def volatility_smile_chart(S, K, T, r, sigma, option_type="call"):
    """
    Generate a synthetic volatility smile chart.

    We create theoretical market prices across different strikes
    and back out implied volatility for each strike.
    """

    strike_range = np.linspace(K * 0.7, K * 1.3, 25)

    implied_vols = []

    for strike in strike_range:

        call_price, put_price = black_scholes(
            S,
            strike,
            T,
            r,
            sigma
        )

        market_price = call_price if option_type == "call" else put_price

        implied_vol = calculate_implied_volatility(
            market_price=market_price,
            S=S,
            K=strike,
            T=T,
            r=r,
            option_type=option_type
        )

        if implied_vol is not None:
            implied_vols.append(implied_vol * 100)
        else:
            implied_vols.append(None)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=strike_range,
            y=implied_vols,
            mode="lines+markers",
            name="Implied Volatility",
            line=dict(
                width=4,
                color=SMILE_COLOR
            ),
            marker=dict(
                size=7
            )
        )
    )

    fig.add_vline(
        x=K,
        line_width=2,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Current Strike",
        annotation_position="top"
    )

    fig.update_layout(
        title={
            "text": "Volatility Smile",
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
            "title": "Strike Price",
            "gridcolor": GRID_COLOR,
            "zerolinecolor": GRID_COLOR
        },
        yaxis={
            "title": "Implied Volatility (%)",
            "gridcolor": GRID_COLOR,
            "zerolinecolor": GRID_COLOR
        },
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