class NoTradeZone:
    def __init__(self, name):
        self.name
        
    @property
    def number_of_shares(self):
        return self._number_of_shares

    @number_of_shares.setter
    def number_of_shares(self, value):
        self._number_of_shares = value
        
    @property
    def number_of_assets(self):
        return self._number_of_assets

    @number_of_assets.setter
    def number_of_assets(self, value):
        self._number_of_assets = value
        
    @property
    def no_trade_zone_width(self):
        return 0.5 / self._number_of_assets