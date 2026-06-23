import numpy as np
import plotly.graph_objects as go


BACKGROUND_COLOR = "#0b1221"
GRID_COLOR = "#24324a"
TEXT_COLOR = "#f8fafc"


def strategy_payoff_chart(strategy, strike):

    prices = np.linspace(
        strike * 0.5,
        strike * 1.5,
        200
    )

    if strategy == "long_call":

        payoff = np.maximum(
            prices - strike,
            0
        )

        title = "Long Call"

    elif strategy == "long_put":

        payoff = np.maximum(
            strike - prices,
            0
        )

        title = "Long Put"

    elif strategy == "straddle":

        call = np.maximum(
            prices - strike,
            0
        )

        put = np.maximum(
            strike - prices,
            0
        )

        payoff = call + put

        title = "Long Straddle"

    elif strategy == "bull_call_spread":

        lower_strike = strike
        upper_strike = strike * 1.1

        long_call = np.maximum(
            prices - lower_strike,
            0
        )

        short_call = -np.maximum(
            prices - upper_strike,
            0
        )

        payoff = long_call + short_call

        title = "Bull Call Spread"

    else:

        payoff = np.zeros_like(prices)

        title = "Strategy"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=prices,
            y=payoff,
            mode="lines",
            line=dict(
                width=4,
                color="#22c55e"
            ),
            name=title
        )
    )

    fig.add_hline(
        y=0,
        line_color="#64748b"
    )

    fig.add_vline(
        x=strike,
        line_dash="dash",
        line_color="#f59e0b",
        annotation_text="Strike"
    )

    fig.update_layout(
        title={
            "text": f"{title} Payoff",
            "x": 0.5
        },
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
        font=dict(
            color=TEXT_COLOR,
            family="Poppins"
        ),
        xaxis=dict(
            title="Underlying Price",
            gridcolor=GRID_COLOR
        ),
        yaxis=dict(
            title="Profit / Loss",
            gridcolor=GRID_COLOR
        ),
        template="plotly_dark",
        margin=dict(
            l=60,
            r=30,
            t=70,
            b=60
        )
    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )