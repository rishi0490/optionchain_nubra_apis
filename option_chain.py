# option_chain.py

from nubra_python_sdk.marketdata.market_data import MarketData
from nubra_python_sdk.marketdata.validation import ExchangeEnum

from config import UNDERLYING, EXPIRY


def fetch_option_chain(client):
    """
    Fetch option chain for configured underlying and expiry.

    Returns:
        OptionChainWrapper
    """

    market = MarketData(client)

    try:
        option_chain = market.option_chain(
            instrument=UNDERLYING,
            expiry=EXPIRY,
            exchange=ExchangeEnum.NSE
        )

        if option_chain is None:
            raise Exception("Option chain API returned None.")

        return option_chain

    except Exception as e:
        print(f"❌ Failed to fetch option chain: {e}")
        raise
