from asset import Asset

class Portfolio:
    def __init__(self, mongoDB):
        self.assets = {
            "GSPC=F": Asset("GSPC=F"),
            "GC=F": Asset("GC=F"),
            "TLT": Asset("TLT"),
            "VIX": Asset("VIX"),
        }
        self.client = mongoDB
        
    @property
    def equity(self):
        return self._equity

    @equity.setter
    def equity(self, value):
        self._equity = value

    @property
    def funds(self):
        return self._funds

    @funds.setter
    def funds(self, value):
        self._funds = value
        
    @property
    def margin(self):
        return self._margin
    
    @margin.setter
    def margin(self, value):
        self._margin = value
    
    @property
    def available(self):
        return self._available
    
    @available.setter
    def available(self, value):
        self._available = value
    
    @property
    def pnl(self):
        return self._pnl
    
    @pnl.setter
    def pnl(self, value):
        self._pnl = value
    
    @property
    def equity_used(self):
        return self._equity_used
    
    @equity_used.setter
    def equity_used(self, value):
        self._equity_used = value

    def update_weights(self):
        for asset in self.assets:
            self.assets[asset].target_weight = self.client.TradingDB.StrategyParameters