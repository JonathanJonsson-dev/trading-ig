#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
IG Markets REST API sample with Python
2015 FemtoTrader
"""

import norgatedata
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
from types import SimpleNamespace

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def fetch_epics(ig_service):
    """
    Min gamla kod som hämtar epics innan jag insåg att det går att gör via filen all_nodes.py
    """
    #search_terms = ["EUR/USD", "Ether", "USA Tech100", "Tyskland 40", "Naturgas", "US Treasury Bond", "3-Month SOFR"]
    search_terms = pd.read_excel('manuell_berakning_minimum_kapital.xlsx', sheet_name="Norgate tickers")['Namn']
    norgate_tickers = pd.read_excel('manuell_berakning_minimum_kapital.xlsx', sheet_name="Norgate tickers")['Code']
    epics = []
    markets_that_got_no_result = []
    search_terms = ["Corn", "Milk", "Lean Hogs", "Live Cattle", "TecDax"]
    
    for term, ticker in zip(search_terms, norgate_tickers):
        print("Söker efter", term)
        df = ig_service.search_markets(term)
        #df = ig_service.search_markets("Corn")
        if len(df) > 0:
            print(df)
            filtered_df = df[(df['instrumentType'] == 'CURRENCIES') | (df['instrumentType'] == 'INDICES') | (df['instrumentType'] == 'COMMODITIES') | (df['instrumentType'] == 'RATES')]
            for _, row in filtered_df.iterrows():
                epics.append({
                    "name": row['instrumentName'],
                    "epic": row['epic'],
                    "norgate ticker": ticker
                    })
            print(filtered_df)
            print(epics)
            print("Antal epics i lista:", len(epics))
            print("Sparar epics till Excel")
            df_epics = pd.DataFrame(epics)
            df_epics.to_excel("epics.xlsx")  
            input("Continue?")
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

    ig_service = IGService(
        config.username,
        config.password,
        config.api_key,
        config.acc_type,
        acc_number=config.acc_number,
    )
    
    ig_service.create_session()
    fetch_epics(ig_service)

if __name__ == "__main__":
    main()
