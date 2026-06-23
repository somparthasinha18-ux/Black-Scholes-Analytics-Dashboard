import math
from scipy.stats import norm


class GreeksCalculator:
    """
    Computes Black-Scholes Greeks for European options.
    """

    def __init__(self, S, K, T, r, sigma):

        self.S = float(S)
        self.K = float(K)
        self.T = float(T)

        self.r = float(r) / 100
        self.sigma = float(sigma) / 100

        self.d1 = (
            math.log(self.S / self.K)
            + (
                self.r
                + 0.5 * self.sigma ** 2
            ) * self.T
        ) / (
            self.sigma * math.sqrt(self.T)
        )

        self.d2 = self.d1 - self.sigma * math.sqrt(self.T)

    # ------------------------
    # Delta
    # ------------------------

    def delta_call(self):

        return norm.cdf(self.d1)

    def delta_put(self):

        return norm.cdf(self.d1) - 1

    # ------------------------
    # Gamma
    # ------------------------

    def gamma(self):

        return (
            norm.pdf(self.d1)
            /
            (
                self.S
                * self.sigma
                * math.sqrt(self.T)
            )
        )

    # ------------------------
    # Vega
    # ------------------------

    def vega(self):

        return (
            self.S
            * norm.pdf(self.d1)
            * math.sqrt(self.T)
        ) / 100

    # ------------------------
    # Theta
    # ------------------------

    def theta_call(self):

        value = (

            (
                -self.S
                * norm.pdf(self.d1)
                * self.sigma
            )

            /

            (
                2
                * math.sqrt(self.T)
            )

            -

            self.r
            * self.K
            * math.exp(-self.r * self.T)
            * norm.cdf(self.d2)

        )

        return value / 365

    def theta_put(self):

        value = (

            (
                -self.S
                * norm.pdf(self.d1)
                * self.sigma
            )

            /

            (
                2
                * math.sqrt(self.T)
            )

            +

            self.r
            * self.K
            * math.exp(-self.r * self.T)
            * norm.cdf(-self.d2)

        )

        return value / 365

    # ------------------------
    # Rho
    # ------------------------

    def rho_call(self):

        return (

            self.K
            * self.T
            * math.exp(-self.r * self.T)
            * norm.cdf(self.d2)

        ) / 100

    def rho_put(self):

        return (

            -self.K
            * self.T
            * math.exp(-self.r * self.T)
            * norm.cdf(-self.d2)

        ) / 100


def calculate_greeks(S, K, T, r, sigma):

    calc = GreeksCalculator(
        S,
        K,
        T,
        r,
        sigma
    )

    return {

        "delta_call": round(calc.delta_call(), 4),

        "delta_put": round(calc.delta_put(), 4),

        "gamma": round(calc.gamma(), 4),

        "vega": round(calc.vega(), 4),

        "theta_call": round(calc.theta_call(), 4),

        "theta_put": round(calc.theta_put(), 4),

        "rho_call": round(calc.rho_call(), 4),

        "rho_put": round(calc.rho_put(), 4)

    }