class Asset:
    def __init__(self, name):
        self._name = name
                       
        self._max_margin_requirement = 0      # Max säkerhetskrav Måste beräkna denna?
        
    @property
    def target_weight(self): # Risk Parity target weight
        return self._target_weight

    @target_weight.setter
    def target_weight(self, value):
        self._target_weight = value
    
    @property
    def total_capital(self): # Totalt kapital
        return self._total_capital 
    
    @total_capital.setter
    def total_capital(self, value):
        self._total_capital = value
    
    @property
    def capital(self): # Kapital
        return self._target_weight * self._total_capital
    
    @property
    def leverage(self): # F
        return self._leverage

    @leverage.setter
    def leverage(self, value):
        self._leverage = value
    
    @property
    def leveraged_capital(self): # Leveraged kapital
        return self.capital * self._leverage
    
    @property
    def margin_requirement_pct(self): # Säkerhetskrav %
        return self._margin_requirement_pct
    
    @margin_requirement_pct.setter
    def margin_requirement_pct(self, value):
        self._margin_requirement_pct = value
        
    @property
    def margin_requirement_sek(self):
        return self._margin_requirement_pct * self.leveraged_capital
    
    @property
    def margin_requirement(self): # Säkerhetskrav
        return self._margin_requirement
    
    @margin_requirement.setter
    def margin_requirement(self, value):
        self._margin_requirement = value
    
    @property
    def contracts(self):
        return self.margin_requirement_sek / self._margin_requirement
    
    @property
    def owned_contracts(self):
        return self._owned_contracts
    
    @owned_contracts.setter
    def owned_contracts(self, value):
        self._owned_contracts = value
    
    @property
    def action(self):
        return self.contracts - self._owned_contracts