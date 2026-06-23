import math
from scipy.stats import norm


class BlackScholes:
    """
    Black-Scholes Option Pricing Model
    """

    def __init__(self, S, K, T, r, sigma):

        self.S = float(S)
        self.K = float(K)
        self.T = float(T)

        # Convert percentages to decimals
        self.r = float(r) / 100
        self.sigma = float(sigma) / 100

    def d1(self):

        return (
            math.log(self.S / self.K)
            + (
                self.r
                + 0.5 * self.sigma ** 2
            ) * self.T
        ) / (
            self.sigma
            * math.sqrt(self.T)
        )

    def d2(self):

        return self.d1() - self.sigma * math.sqrt(self.T)

    def call_price(self):

        d1 = self.d1()
        d2 = self.d2()

        return (
            self.S * norm.cdf(d1)
            - self.K
            * math.exp(-self.r * self.T)
            * norm.cdf(d2)
        )

    def put_price(self):

        d1 = self.d1()
        d2 = self.d2()

        return (
            self.K
            * math.exp(-self.r * self.T)
            * norm.cdf(-d2)
            - self.S
            * norm.cdf(-d1)
        )


def black_scholes(S, K, T, r, sigma):
    """
    Wrapper function used by Flask.
    Returns rounded Call and Put prices.
    """

    model = BlackScholes(
        S,
        K,
        T,
        r,
        sigma
    )

    call = round(model.call_price(), 4)
    put = round(model.put_price(), 4)

    return call, put