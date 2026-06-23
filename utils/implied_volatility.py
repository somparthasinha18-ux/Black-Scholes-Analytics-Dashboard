from utils.black_scholes import black_scholes


def calculate_implied_volatility(
    market_price,
    S,
    K,
    T,
    r,
    option_type="call",
    tolerance=1e-6,
    max_iterations=100
):
    """
    Calculate implied volatility using the bisection method.

    Returns:
        float | None
    """

    if market_price <= 0:
        return None

    if option_type not in ["call", "put"]:
        return None

    low_vol = 0.0001
    high_vol = 3.0      # 300% maximum

    for _ in range(max_iterations):

        mid_vol = (low_vol + high_vol) / 2

        call_price, put_price = black_scholes(
            S,
            K,
            T,
            r,
            mid_vol
        )

        model_price = (
            call_price
            if option_type == "call"
            else put_price
        )

        difference = model_price - market_price

        if abs(difference) < tolerance:

            # reject unrealistic IV
            if mid_vol > 3.0:
                return None

            return mid_vol

        if difference > 0:
            high_vol = mid_vol
        else:
            low_vol = mid_vol

    # Solver did not converge
    if mid_vol > 3.0:
        return None

    return mid_vol