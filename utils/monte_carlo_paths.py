import numpy as np
import plotly.graph_objects as go


BACKGROUND_COLOR = "#0b1221"
GRID_COLOR = "#24324a"
TEXT_COLOR = "#f8fafc"


def monte_carlo_path_chart(
    S,
    T,
    r,
    sigma,
    paths=100,
    steps=252,
    random_seed=42
):
    """
    Generate Monte Carlo stock price paths using Geometric Brownian Motion.
    """

    np.random.seed(random_seed)

    r_decimal = r / 100
    sigma_decimal = sigma / 100

    dt = T / steps

    time_grid = np.linspace(0, T, steps + 1)

    price_paths = np.zeros((steps + 1, paths))
    price_paths[0] = S

    for step in range(1, steps + 1):

        z = np.random.standard_normal(paths)

        price_paths[step] = price_paths[step - 1] * np.exp(
            (r_decimal - 0.5 * sigma_decimal ** 2) * dt
            + sigma_decimal * np.sqrt(dt) * z
        )

    fig = go.Figure()

    for path in range(paths):
        fig.add_trace(
            go.Scatter(
                x=time_grid,
                y=price_paths[:, path],
                mode="lines",
                line=dict(
                    width=1
                ),
                opacity=0.35,
                showlegend=False
            )
        )

    fig.add_trace(
        go.Scatter(
            x=time_grid,
            y=np.mean(price_paths, axis=1),
            mode="lines",
            name="Average Path",
            line=dict(
                width=4,
                color="#f59e0b"
            )
        )
    )

    fig.update_layout(
        title={
            "text": "Monte Carlo Simulated Price Paths",
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
            "title": "Time to Expiry (Years)",
            "gridcolor": GRID_COLOR,
            "zerolinecolor": GRID_COLOR
        },
        yaxis={
            "title": "Simulated Stock Price",
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