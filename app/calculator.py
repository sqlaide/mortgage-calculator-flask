import pandas as pd
import numpy as np
from datetime import date
import numpy_financial as npf


class MortgageCalculator:
  def __init__(self, loan_amount: int, interest_rate, down_payment: int, hoa: int, property_taxes: int) -> None:
    self.down_payment = down_payment
    self.hoa = hoa
    self.interest_rate = interest_rate
    self.loan_amount = loan_amount
    self.period = 360
    self.n_periods = np.arange(self.period) + 1
    self.property_taxes = property_taxes
    self.hoa = hoa

  @property
  def interest_rate(self):
    """
    docstring
    """
    return self._interest_rate
  
  @interest_rate.setter
  def interest_rate(self, rate):
    if rate > 0 and rate <10:
      self._interest_rate = (rate  /100)/12
    else:
      raise ValueError("Rate should between 1% and 10%")

  @property
  def loan_amount(self):
    return self._loan_amount

  @loan_amount.setter
  def loan_amount(self, amount):
    if self.down_payment:
      self._loan_amount = -(amount - self.down_payment)
    else:
      self._loan_amount = -(amount)

  def amortization_table(self):
    # CREATE ARRAY
    df_initialize = list(zip(self.n_periods, self.monthly_interest(), self.monthly_principal()))
    df = pd.DataFrame(df_initialize, columns=['period','interest','principal'])
    df['monthly_payment'] = df['interest'] + df['principal']
    
  # CALCULATE CUMULATIVE SUM OF MORTAGE PAYMENTS
    df['outstanding_balance'] = df['monthly_payment'].cumsum()
    
  # REVERSE VALUES SINCE WE ARE PAYING DOWN THE BALANCE
    df.outstanding_balance = df.outstanding_balance.values[::-1]
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