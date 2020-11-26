import pandas as pd
import numpy as np
# from datetime import date
import numpy_financial as npf
from datetime import datetime
from typing import Optional


class MortgageCalculator:
    def __init__(
      self,
      loan_amount: float,
      interest_rate: float,
      down_payment: Optional[float],
      hoa: Optional[int],
      property_taxes: Optional[float],
      start_date: Optional[datetime],
      period: int = 360) -> None:
        self.down_payment = down_payment
        self.hoa = hoa
        self.interest_rate = interest_rate
        self.loan_amount = loan_amount
        self.period = period
        self.n_periods = np.arange(self.period) + 1
        self.property_taxes = property_taxes
        self.hoa = hoa
        self.n_period_months = None
        self.start_date = start_date or datetime.today().strftime("%Y-%m-%d")

    @property
    def interest_rate(self):
        return self._interest_rate

    @interest_rate.setter 
    def interest_rate(self, rate):
        if rate > 0 and rate < 10:
            self._interest_rate = (rate / 100)/12
        else:
            raise ValueError("Rate should between 1% and 10%")

    @property
    def loan_amount(self):
        return self._loan_amount

    @loan_amount.setter
    def loan_amount(self, amount):
        if self.down_payment:
          if (self.down_payment > 0 and self.down_payment <= amount):
            self._loan_amount = -(amount - self.down_payment)
          else:
            raise ValueError("Down Payment cannot be greater than loan amount")
        else:
            self._loan_amount = -(amount)

    def amortization_table(self): 
        # CREATE ARRAY
        date_range = pd.date_range(start=self.start_date, periods=self.period, freq='M', end=None)
        df_initialize = list(
            zip(self.n_periods, date_range, self.monthly_interest(), self.monthly_principal()))
        df = pd.DataFrame(df_initialize, columns=[
                          'Period', 'Date', 'Interest', 'Principal'], index=date_range)
        df['PMI'] = df['Interest'] + df['Principal']

    # CALCULATE CUMULATIVE SUM OF MORTAGE PAYMENTS
        df['Balance'] = df['PMI'].cumsum()

    # REVERSE VALUES SINCE WE ARE PAYING DOWN THE BALANCE
        df.Balance = df.Balance.values[::-1]
        pd.set_option('precision', 2)
        return df

    def monthly_interest(self):
        # for 30 years fixed
        return npf.ipmt(self.interest_rate, self.n_periods, self.period, self.loan_amount)

    def monthly_principal(self):
        return npf.ppmt(self.interest_rate, self.n_periods, self.period, self.loan_amount)

    def monthly_payment(self):
        pmi = npf.pmt(self.interest_rate, self.period, self.loan_amount)
        if self.property_taxes:
            pmi += self.property_taxes
        if self.hoa:
            pmi += self.hoa
        return '${:,.2f}'.format(pmi)
