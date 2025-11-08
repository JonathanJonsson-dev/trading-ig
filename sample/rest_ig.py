#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
IG Markets REST API sample with Python
2015 FemtoTrader
"""

from trading_ig import IGService
from trading_ig.config import config
import logging

# if you need to cache to DB your requests
from datetime import timedelta
import requests_cache
import time
import pandas as pd
import random 
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def fetch_epics(ig_service):
    """
    Min gamla kod som hämtar epics innan jag insåg att det går att gör via filen all_nodes.py
    """
    search_terms = ["EUR/USD", "Ether", "USA Tech100", "Tyskland 40", "Naturgas", "US Treasury Bond", "3-Month SOFR"]
    #search_terms = pd.read_excel('ig_markets_marknader.xlsx', sheet_name="Blad2")['Namn']
    
    search_terms = pd.read_excel('ig_markets_marknader.xlsx', sheet_name="Norgate tickers")['Namn']
    #search_terms = ["Australian Dollar", "British Pound", "Canadian Dollar", "Euro FX", "E-mini S&P 500", "Nasdaq 100"]
    epics = []
    markets_that_got_no_result = []
    
    for term in search_terms:
        print("Söker efter", term)
        df = ig_service.search_markets(term)
        if len(df) > 0:
            print(df)
            filtered_df = df[(df['instrumentType'] == 'CURRENCIES') | (df['instrumentType'] == 'INDICES') | (df['instrumentType'] == 'COMMODITIES') | (df['instrumentType'] == 'RATES')]
            for epic in filtered_df['epic']:
                epics.append(epic)
            print(filtered_df)
            print(epics)
            print("Antal epics i lista:", len(epics))
            print("Sparar epics till Excel")
            df_epics = pd.DataFrame(epics)
            df_epics.to_excel("epics.xlsx")  
        else:
            markets_that_got_no_result.append(term)
        time.sleep(random.randint(5, 15))
    print(epics)
    print("\nNorgate markets_that_got_no_result", markets_that_got_no_result)

def main():
    logging.basicConfig(level=logging.DEBUG)

    expire_after = timedelta(hours=1)
    session = requests_cache.CachedSession(
        cache_name="cache", backend="sqlite", expire_after=expire_after
    )

    print(session.headers)
    # set expire_after=None if you don't want cache expiration
    # set expire_after=0 if you don't want to cache queries

    # config = IGServiceConfig()

    # no cache
    ig_service = IGService(
        config.username,
        config.password,
        config.api_key,
        config.acc_type,
        acc_number=config.acc_number,
    )

    # if you want to globally cache queries
    # ig_service = IGService(config.username, config.password, config.api_key,
    #   config.acc_type, session)

    ig_service.create_session()
    # ig_stream_service.create_session(version='3')

    accounts = ig_service.fetch_accounts()
    print("accounts:\n%s" % accounts)

    # account_info = ig_service.switch_account(config.acc_number, False)
    # print(account_info)

    # open_positions = ig_service.fetch_open_positions()
    # print("open_positions:\n%s" % open_positions)

    print("")

    # working_orders = ig_service.fetch_working_orders()
    # print("working_orders:\n%s" % working_orders)

    print("")
    
    epic = "IX.D.ASX.IFM.IP"  # US (SPY) - mini
    
    #print(ig_service.search_markets("EUR/USD"))
    
    epics = pd.read_excel('epics.xlsx')['epic']
    for epic in epics:
        print(epic)
        data = ig_service.fetch_market_by_epic(epic)
        print(data)
        print(json.dumps(data, indent=2, sort_keys=True))
        time.sleep(random.randint(5, 15))
        
    
    resolution = "D"
    # see from pandas.tseries.frequencies import to_offset
    # resolution = 'H'
    # resolution = '1Min'

    num_points = 10
    #response = ig_service.fetch_historical_prices_by_epic_and_num_points(
    #    epic, resolution, num_points
    #)
    #print(response)
    # Exception: error.public-api.exceeded-account-historical-data-allowance

    # if you want to cache this query
    # response = ig_service.fetch_historical_prices_by_epic_and_num_points(
    #   epic, resolution, num_points, session
    # )

    # df_ask = response['prices']['ask']
    # print("ask prices:\n%s" % df_ask)

    # (start_date, end_date) = ('2015-09-15', '2015-09-28')
    # response = ig_service.fetch_historical_prices_by_epic_and_date_range(
    #   epic, resolution, start_date, end_date
    # )

    # if you want to cache this query
    # response = ig_service.fetch_historical_prices_by_epic_and_date_range(
    #   epic, resolution, start_date, end_date, session
    # )
    # df_ask = response['prices']['ask']
    # print("ask prices:\n%s" % df_ask)


if __name__ == "__main__":
    main()
