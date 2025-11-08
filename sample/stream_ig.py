import sys
import logging
import os

from lightstreamer.client import (
    LightstreamerClient,
    Subscription,
    ConsoleLoggerProvider,
    ConsoleLogLevel,
    SubscriptionListener,
    ItemUpdate,
)

from trading_ig import IGService, IGStreamService
from trading_ig.config import config
from sample.sample_utils import crypto_epics, wait_for_input, futures_epics
from sample.portfolio import Portfolio
#import pymongo

logger = logging.getLogger(__name__)

loggerProvider = ConsoleLoggerProvider(ConsoleLogLevel.INFO)
LightstreamerClient.setLoggerProvider(loggerProvider)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(message)s",
)

#portfolio = Portfolio(pymongo.MongoClient(os.getenv('MONGODB_CONNECTIONSTRING')))

def ig_stream_sample():
    ig_service = IGService(
        config.username,
        config.password,
        config.api_key,
        config.acc_type,
        acc_number=config.acc_number,
    )
    #ig_service.create_session() # Skapar en rest session.
    
    ig_stream_service = IGStreamService(ig_service)
    ig_stream_service.create_session()
    # ig_stream_service.create_session(version='3')

    # create a new MARKET Subscription
    #market_subscription = Subscription(
    #    mode="MERGE",
    #    # fx_epics, index_epics, weekend_epics, futures_epics, cfd_fx_epics
    #    items=[f"MARKET:{epic}" for epic in futures_epics], #IX.D.SUNNAS.IFE.IP
    #    fields=[
    #        "UPDATE_TIME",
    #        "BID",
    #        "OFFER",
    #        "CHANGE",
    #        "MARKET_STATE",
    #        "CHANGE_PCT",
    #        "HIGH",
    #        "LOW",
    #    ],
    #)
    # Define the EPIC you want to subscribe to
    epic = 'IX.D.SUNNAS.IFE.IP'

    # Create a subscription object
    market_subscription = Subscription(
        mode="MERGE",
        items=["MARKET:" + epic],
        fields=["BID", "OFFER", "HIGH", "LOW", "CHANGE", "MARKET_STATE"]
        )
    # adding a listener to MARKET subscription
    #market_subscription.addListener(MarketListener(portfolio))

    # registering the MARKET subscription
    #ig_stream_service.subscribe(market_subscription)

    ### create a new ACCOUNT subscription ###
    account_subscription = Subscription(
        mode="MERGE",
        items=[f"ACCOUNT:{config.acc_number}"],
        fields=["FUNDS", "MARGIN", "AVAILABLE_TO_DEAL", "PNL", "EQUITY", "EQUITY_USED"],
    )

    # adding a listener to ACCOUNT subscription
    account_subscription.addListener(AccountListener(portfolio))

    # registering the ACCOUNT subscription
    ig_stream_service.subscribe(account_subscription)

    ### create a new TRADE Subscription ###
    trade_subscription = Subscription(
        mode="DISTINCT",
        items=[f"TRADE:{config.acc_number}"],
        fields=["CONFIRMS", "OPU", "WOU"],
    )

    # adding a listener to TRADE subscription
    #trade_subscription.addListener(TradeListener())

    # registering the TRADE subscription
    #ig_stream_service.subscribe(trade_subscription)

    # await updates
    wait_for_input()
    
    # disconnecting
    ig_stream_service.disconnect()


class MarketListener(SubscriptionListener):
    def __init__(self, portfolio):
        self.portfolio = portfolio
        
    def onItemUpdate(self, update: ItemUpdate):
        logger.info(
            f"{update.getValue('UPDATE_TIME')} {update.getItemName()} "
            f"Bid: {update.getValue('BID')}, "
            f"Offer: {update.getValue('OFFER')}, "
            f"Price change: {update.getValue('CHANGE')}, "
            f"State: {update.getValue('MARKET_STATE')}, "
            f"Change: {update.getValue('CHANGE_PCT')}%, "
            f"High: {update.getValue('HIGH')}, "
            f"Low: {update.getValue('LOW')}"
        )
        spy = portfolio.assets.get("GSPC=F")
        spy.target_weight = 0.5372
        spy.total_capital = 214131
        spy.leverage = 10
        spy.margin_requirement_pct = 0.05
        spy.margin_requirement = 127355.11
        spy.owned_contracts = 0.47
        print(spy.action)

    def onSubscription(self):
        logger.info("MarketListener onSubscription()")

    def onSubscriptionError(self, code, message):
        logger.info(f"MarketListener onSubscriptionError(): '{code}' {message}")

    def onUnsubscription(self):
        logger.info("MarketListener onUnsubscription()")


class AccountListener(SubscriptionListener):
    def __init__(self, portfolio):
        self.portfolio = portfolio
    
    def onItemUpdate(self, update: ItemUpdate):
        logger.info(
            f"{update.getItemName()} "
            f"Funds: {update.getValue('FUNDS')}, "
            f"Margin: {update.getValue('MARGIN')}, "
            f"Available: {update.getValue('AVAILABLE_TO_DEAL')}, "
            f"P&L: {update.getValue('PNL')}, "
            f"Equity: {update.getValue('EQUITY')}, "
            f"Equity used: {update.getValue('EQUITY_USED')}%"
        )
        self.portfolio.funds = float(update.getValue('FUNDS'))
        self.portfolio.margin = float(update.getValue('MARGIN'))
        self.portfolio.available = float(update.getValue('AVAILABLE_TO_DEAL'))
        self.portfolio.pnl = float(update.getValue('PNL'))
        self.portfolio.equity = float(update.getValue('EQUITY'))
        self.portfolio.equity_used = float(update.getValue('EQUITY_USED'))
        
        print(self.portfolio.funds)

    def onSubscription(self):
        logger.info("AccountListener onSubscription()")

    def onSubscriptionError(self, code, message):
        logger.info(f"AccountListener onSubscriptionError(): '{code}' {message}")

    def onUnsubscription(self):
        logger.info("AccountListener onUnsubscription()")


class TradeListener(SubscriptionListener):
    def onItemUpdate(self, update: ItemUpdate):
        logger.info(
            f"{update.getItemName()} "
            f"Confirms: {update.getValue('CONFIRMS')}, "
            f"Open position updates: {update.getValue('OPU')}, "
            f"Working order updates: {update.getValue('WOU')}, "
        )

    def onSubscription(self):
        logger.info("TradeListener onSubscription()")

    def onSubscriptionError(self, code, message):
        logger.info(f"TradeListener onSubscriptionError(): '{code}' {message}")

    def onUnsubscription(self):
        logger.info("TradeListener onUnsubscription()")


if __name__ == "__main__":
    ig_stream_sample()
